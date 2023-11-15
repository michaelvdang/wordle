import React, {createRef, useEffect, useState, useRef} from 'react'
import NewGameDialog from './NewGameDialog'
import UsernameDialog from './UsernameDialog'
import NavBar from './NavBar'
import StatsDialog from './StatsDialog'
import LeaderboardModal from './LeaderboardModal'
import ErrorDialog from './ErrorDialog'

const LETTERS = [
  ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
  ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
  ['Z', 'X', 'C', 'V', 'B', 'N', 'M']
]

const KEYS = [
  [0,1,2,3,4],[5,6,7,8,9],[10,11,12,13,14],[15,16,17,18,19],[20,21,22,23,24],[25,26,27,28,29]
]

const GUESSES = [
  'angry', 'happy', 'cloud', 'viper', 'sheer', 'house'
]

const Wordle = () => {

  const [username, setUsername] = useState('mdang');
  const [isSettingUsername, setIsSettingUsername] = useState(false);
  const [showStats, setShowStats] = useState(false);
  const [showLeaderboard, setShowLeaderboard] = useState(false);
  const [guesses, setGuesses] = useState([]);       // array of made guesses
  const [guessIndex, setGuessIndex] = useState(0);  // index of the current guess
  // const [letterIndex, setLetterIndex] = useState(0);
  const [currentGuess, setCurrentGuess] = useState(''); // current guess being made
  const [gameWon, setGameWon] = useState(false);
  const [gameCompleted, setGameCompleted] = useState(false);
  const [isNewGame, setIsNewGame] = useState(false);
  const [invalidWord, setInvalidWord] = useState(false);
  const [game, setGame] = useState({
    game_id: '',
    username: '',
    guid: '',
    user_id: '',
    remain: 0,
    guesses: [],
    absent_letters: [],
    present_letters: [],
    correct_letters: '',
    completed: false,
    won: false,
    answer: '',
  });
  const mainRef = createRef(null);
  const inputRef = useRef(null);
  const [hasFocus, setHasFocus] = useState(true);
  const [hasError, setHasError] = useState(false);

  const fetchNewGame = () => {
    // fetch('http://mikespace.xyz:9400/game/new?username=' + username,
    // fetch('http://localhost:9400/game/new?username=' + username,
    fetch('https://orchestrator.api.mikespace.xyz/game/new?username=' + username,
      {
        method: 'POST',
      })
      .then(response => response.json())
      .then(data => setGame({
        game_id: data.game_id,
        username: username,
        guid: data.guid,
        user_id: data.user_id,
        remain: parseInt(data.remain),
        guesses: [],
        absent_letters: '',
        present_letters: '',
        correct_letters: '*****',
        completed: false,
        won: false,
      }))
      .catch(err => {
        console.log(err);
        setHasError(true);
      })
  }

  // first page load, start new game with username
  useEffect(() => {
    if (username === '') {
      setIsSettingUsername(true);
    }
    setGuesses([]);
    setGuessIndex(0);
    setCurrentGuess('');
    mainRef.current.focus();      // focus on main when first page load
    // console.log('component did mount');
    
    window.scrollTo(-50, 0)

  }, [])

  // find a better way to detect when new username is entered 
  // only fetchNewGame for new username
  useEffect(() => {
    if (!isSettingUsername && username !== '') {
      setGuesses([]);
      setGuessIndex(0);
      setCurrentGuess('');
      fetchNewGame();
      setTimeout(() => {
        inputRef.current.focus();
      }, 500);
    }
    // console.log('isSettingUsername updated');
  }, [isSettingUsername])

  // reset and start new game
  useEffect(() => {
    if (isNewGame) {
      setGuesses([]);
      setGuessIndex(0);
      setCurrentGuess('');
      setGameWon(false);
      setGameCompleted(false);
      setIsNewGame(false);
      fetchNewGame();
      setTimeout(() => {
        inputRef.current.focus();
      }, 500);
      return;
    }
  }, [isNewGame])
  
  // return focus to input after closing Stats and Leaderboard
  useEffect(() => { 
    if (!showStats && !showLeaderboard) {
      setTimeout(() => {
        inputRef.current.focus();
      }, 500);
    }
  }, [showStats, showLeaderboard])

  const handleClick = () => {
    setGuesses([...guesses, GUESSES[guessIndex]]);
    setGuessIndex(guessIndex + 1);
  }

  // useEffect(() => {
  //   console.log('game: ', game);
  // }, [game])
  
  
  const handleValidWord = (data) => {
    // update game
    // update correct, present, and absent letters
    const results = data['guess_results'];
    let correct_letters = '';
    let present_letters = game.present_letters;
    let absent_letters = game.absent_letters;
    for (let i = 0; i < results.length; i++) {
      // update absent, present, and correct letters in game object
      if (results[i] === 0 && !absent_letters.includes(currentGuess[i])) absent_letters += currentGuess[i];
      if (results[i] >= 1 && !present_letters.includes(currentGuess[i])) present_letters += currentGuess[i];
      if (results[i] === 2 && game.correct_letters[i] === '*') correct_letters += currentGuess[i];
      else correct_letters += game.correct_letters[i];
    }
    setGame({
      ...game,
      'remain': parseInt(data.remain),
      'guesses': [...game.guesses, data['guess' + (guessIndex + 1)]],
      correct_letters,
      absent_letters,
      present_letters,
      'won': data['won'],
      'completed': data['completed'],
      'answer': data['answer'] ? data['answer'] : '',
    })
    setGuesses(() => [...guesses, currentGuess]);
    setGuessIndex(guessIndex + 1);
    setCurrentGuess('');
    
    // TODO: add 'complete' to Orc API or will get error for results.length
    if (data['completed']) {
      setGameCompleted(true);
      // console.log('GAME COMPLETED: DID YOU WIN? ', data['won'])
      if (data['won']) {
        setGameWon(true);
        // start new game?
        return;
      }
    }
  }
  
  // refocus to next input after submitting a guess
  useEffect(() => {
    if (guessIndex < 6) // there will not be a 7th inputRef
      inputRef.current.focus();
  }, [guessIndex])

  const handleKeyDown = (e) => {
    // console.log('localStorage: ', localStorage)
    if (guesses.length > 5) return;
    if (e.key === 'Backspace') {
      setCurrentGuess(currentGuess.slice(0, -1));
      setInvalidWord(false); // remove error style highlight
      // setGameCompleted(true); // for testing only
      return;
    }
    if (currentGuess.length > 4) {  // only register 'Enter' when there are 5 characters in guess
      if (e.key === 'Enter') {
        // fetch('http://mikespace.xyz:9400/game/' + game.game_id + '?username=' + username + '&guid=' + game.guid + '&user_id=' + game.user_id + '&guess=' + currentGuess,
        // fetch('http://localhost:9400/game/' + game.game_id + '?username=' + username + '&guid=' + game.guid + '&user_id=' + game.user_id + '&guess=' + currentGuess,
        fetch('https://orchestrator.api.mikespace.xyz/game/' + game.game_id + '?username=' + username + '&guid=' + game.guid + '&user_id=' + game.user_id + '&guess=' + currentGuess,
          {
            method: 'POST',
          })
          .then(response => response.json())
          .then(data => {
            // console.log('data: ', data);
            // word is valid
            if (data['status'] === 'success')
              handleValidWord(data);
            // word is not valid
            else{
              setInvalidWord(true);
            }
            // start new game
            if (data.completed)
              setGameCompleted(true);
          })
          .catch(err => {
            console.log(err);
            setHasError(true);
          })
        return;
      }
      return;
    }
    if (e.keyCode >= 65 && e.keyCode <= 90) { // only register letters
      setCurrentGuess(currentGuess => currentGuess + e.key.toLowerCase());
    }
  }

  const bubbleStyle = 'flex items-center justify-center \
                        rounded-full cursor-default select-none \
                        w-14 h-14 text-xl\
                        sm:w-20 sm:h-20 sm:text-3xl \
                        md:w-28 md:h-28 md:text-6xl md:pb-2 \
                        font-bold font-serif \
                        ';
  const smallBubbleStyle = 'flex items-center justify-center \
                        cursor-default select-none rounded-3xl \
                        w-6 h-6 text-[10px] \
                        sm:w-8 sm:h-8 sm:text-xs \
                        md:w-10 md:h-10 md:text-sm md:pb-1 \
                        font-bold font-serif \
                        ';
  const errorStyle = 'shadow-[0_0_5px_7px_rgba(0,0,0,0.3)] shadow-red-500 ';
  const regularStyle = 'text-gray-700 bg-gray-200 dark:text-gray-800 dark:bg-red ';
  const absentLetterStyle = 'bg-gray-500 ';
  const presentLetterStyle = 'bg-blue-300';
  const correctLetterStyle = 'bg-green-300 ';
  const focusStyle = 'shadow-[0_0_5px_7px_rgba(0,0,0,0.3)] shadow-gray-400';
  
  // const bubbleStyle = 'flex items-center justify-center \
  //                       rounded-full cursor-default select-none \
  //                       w-14 h-14 text-xl\
  //                       sm:w-20 sm:h-20 sm:text-3xl \
  //                       md:w-28 md:h-28 md:text-6xl md:pb-2 \
  //                       font-bold font-serif \
  //                       ';
  // const smallBubbleStyle = 'flex items-center justify-center \
  //                       cursor-default select-none rounded-3xl \
  //                       w-6 h-6 text-[10px] \
  //                       sm:w-8 sm:h-8 sm:text-xs \
  //                       md:w-10 md:h-10 md:text-sm md:pb-1 \
  //                       font-bold font-serif \
  //                       ';
  // const errorStyle = 'shadow-[0_0_5px_7px_rgba(0,0,0,0.3)] shadow-red-500 ';
  // const regularStyle = 'text-gray-700 bg-gray-300 dark:text-gray-800 dark:bg-white ';
  // const absentLetterStyle = 'bg-gray-500 ';
  // const presentLetterStyle = 'bg-blue-300';
  // const correctLetterStyle = 'bg-green-300 ';
  // const focusStyle = 'shadow-[0_0_5px_7px_rgba(0,0,0,0.3)] shadow-gray-400';

  return (
    <>
    {isSettingUsername && 
      <UsernameDialog 
        username={username}
        setUsername={setUsername} 
        setIsSettingUsername={setIsSettingUsername}
        // mainRef={mainRef}
      />
    }
    {(game.completed) && // problem is this is not getting the latest game object
      <NewGameDialog
        gameCompleted={gameCompleted} 
        setGameCompleted={setGameCompleted}
        setIsNewGame={setIsNewGame}
        answer={game.answer}
        won={game.won}
        numGuesses={guessIndex}
      />
    }
    {showStats && 
      <StatsDialog 
        setShowStats={setShowStats}
        username={username}
        user_id={game.user_id}
      />
    }
    {showLeaderboard && 
      <LeaderboardModal 
        setShowLeaderboard={setShowLeaderboard}
      />
    }
    {hasError && 
      <ErrorDialog
        hasError={hasError}
        setHasError={setHasError}
      />
    }
    <NavBar 
      setIsNewGame={setIsNewGame}
      setShowStats={setShowStats}
      setShowLeaderboard={setShowLeaderboard}
      username={username}
      setIsSettingUsername={setIsSettingUsername}
    />
    <main 
      className="flex flex-col items-center justify-center pt-12 dark" 
      onKeyDown={handleKeyDown}
      onFocus={() => {inputRef.current.focus(); setHasFocus(true);}}
      onBlur={() => setHasFocus(false)}
      tabIndex={0}
      ref={mainRef}
      >
      <div className='grid grid-rows-6 gap-2 mb-12 sm:mb-18 md:mb-24'>
        {[0,1,2,3,4,5].map((i) => (
          <div key={i} className='grid grid-cols-5 gap-2'>
            {guesses[i] 
              // if rendering past guesses
              ? guesses[i].split('').map((letter, index) => (
                  // absent letter
                  (game.absent_letters.includes(letter.toLowerCase()) 
                  ? <div key={KEYS[i][index]}
                      className={`${bubbleStyle} ${absentLetterStyle}`}
                    >
                      {letter}
                    </div>
                  // correct letter
                  : (game.correct_letters.includes(letter.toLowerCase()) && letter === game.correct_letters[index]
                    ? <div key={KEYS[i][index]}
                        className={`${bubbleStyle} ${correctLetterStyle}`}
                      >
                        {letter}
                      </div>
                    // present letter
                    : <div key={KEYS[i][index]}
                        className={`${bubbleStyle} ${presentLetterStyle}`}
                      >
                        {letter}
                      </div>
                    )
                  )
                ))
              // else: if rendering current guess
              : 
                <>
                  {
                    guessIndex === i &&         
                    <input 
                      id='mainId'
                      ref={inputRef}
                      autoComplete='off'
                      autoCapitalize='off'
                      className='absolute -left-80'
                      type="email" 
                      maxLength={5}
                      value={currentGuess} 
                      onChange={() => {}}
                      />
                    }
                  {(currentGuess && guessIndex === i)
                    ? (currentGuess.length === 5)      
                      // highlight all five characters if there are 5 letters in currentGuess
                      ? currentGuess.split('').map((letter, index) => (
                          <div key={KEYS[i][index]} 
                              className={`${bubbleStyle} ${regularStyle}
                                ${hasFocus 
                                  ? (invalidWord ? errorStyle : focusStyle) 
                                  : ''}
                              `} // find the column to highlight the incoming letter of current guess, style invalid words
                              //   ${hasFocus ? focusStyle : ''}
                              // ${invalidWord && errorStyle}`} // find the column to highlight the incoming letter of current guess, style invalid words
                            >
                              {letter}
                            </div> 
                          )) 
                      // otherwise only highlight incoming letter
                      : currentGuess.padEnd(5, ' ').split('').map((letter, index) => (
                          <div key={KEYS[i][index]} 
                            className={`${bubbleStyle} ${regularStyle}
                            ${index === currentGuess.length
                              ? (hasFocus ? focusStyle : '') 
                              : ''}` } // find the column to highlight the incoming letter of current guess
                          >
                            {letter}
                          </div> 
                          ))
                    // else: not current guess, rendering blank spaces
                    : '     '.split('').map((space, index) => (
                      <div key={KEYS[i][index]} 
                        className={`${bubbleStyle} ${regularStyle}
                          ${i === guesses.length && index === 0 && hasFocus
                            ? focusStyle
                            : ''} 
                          `} // highlight first box for new guess
                      >
                        {space}
                      </div>
                      ))}
                </>
              
            }
          </div>
        ))}
      </div>
        {/* input box to open keyboard on ios, remove outline, input-bg and text same color as container bg */}
      {/* <div>
        <input 
          ref={inputRef} 
          className="h-1 focus:outline-none bg-[#242424] text-[#242424] -z-10" 
          type="email" 
          maxLength={5}
          value={currentGuess} 
          onChange={() => {}}
          />
      </div> */}
      <div className='flex flex-col items-center justify-center gap-2'>
        {LETTERS.map((row) => (
          <div key={row} className='flex flex-row gap-1'>
            {row.map((i) => (
              (game.absent_letters.includes(i.toLowerCase())
              ? <div key={i} className={`${smallBubbleStyle} ${absentLetterStyle}`}>
                  {i}
                </div>
              : (game.correct_letters.includes(i.toLowerCase())
                ? <div key={i} className={`${smallBubbleStyle} ${correctLetterStyle}`}>
                    {i}
                  </div>
                : (game.present_letters.includes(i.toLowerCase())
                  ? <div key={i} className={`${smallBubbleStyle} ${presentLetterStyle}`}>
                      {i}
                    </div>
                  : <div key={i} className={`${smallBubbleStyle} ${regularStyle}`}>
                      {i}
                    </div>
                  )
                )
              )
              // // used to work and then it didn't for some reason
              // <div key={i} className={`flex items-center justify-center bg-white 
              // cursor-default select-none rounded-3xl
              // text-gray-800 w-10 h-10 font-bold text-sm pb-1 font-serif
              // ${game.absent_letters.includes(i.toLowerCase()) ? absentLetterStyle : ''}
              // ${game.present_letters.includes(i.toLowerCase()) ? presentLetterStyle : ''}
              // ${game.correct_letters.includes(i.toLowerCase()) ? correctLetterStyle : ''}
              // `}>
              //   {i}
              // </div>
            ))}
          </div>
        ))}
      </div>
      
    </main>
    </>
  )
}

export default Wordle