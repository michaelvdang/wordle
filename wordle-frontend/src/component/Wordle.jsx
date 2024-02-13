import React, {createRef, useEffect, useState, useRef, useCallback} from 'react'
import NewGameDialog from './NewGameDialog'
import UsernameDialog from './UsernameDialog'
import NavBar from './NavBar'
import StatsDialog from './StatsDialog'
import LeaderboardModal from './LeaderboardModal'
import ErrorDialog from './ErrorDialog'
import AboutModal from './AboutModal'

let STATS_URL = ''
let ORC_URL = ''
if (import.meta.env.VITE_DOMAIN_NAME === undefined) {
  throw new Error('Missing env file or env variables');
}
const VITE_DOMAIN_NAME = import.meta.env.VITE_DOMAIN_NAME // 'michaeldang.dev'
const VITE_SERVER_IP = '' + import.meta.env.VITE_SERVER_IP
// check if a real domain name is supplied
if (import.meta.env.DEV || VITE_DOMAIN_NAME == 'no-domain') {
  STATS_URL = 'http://localhost:9000'
  ORC_URL = 'http://localhost:9400'
}
// else if (import.meta.env.VITE_DOMAIN_NAME == 'no-domain') {
//   // STATS_URL = '/wordle'
//   // ORC_URL = '/wordle'
//   STATS_URL = VITE_SERVER_IP + ':9000'
//   ORC_URL = VITE_SERVER_IP + ':9400'
// }
else {
  STATS_URL = 'https://stats.api.' + VITE_DOMAIN_NAME
  ORC_URL = 'https://orchestrator.api.' + VITE_DOMAIN_NAME
}

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

const Wordle = ({mode}) => {
  const [username, setUsername] = useState('');
  const [isSettingUsername, setIsSettingUsername] = useState(false);
  const [showAbout, setShowAbout] = useState(false);
  const [showStats, setShowStats] = useState(false);
  const [showLeaderboard, setShowLeaderboard] = useState(false);
  const [guesses, setGuesses] = useState([]);       // array of made guesses
  const [guessIndex, setGuessIndex] = useState(0);  // index of the current guess
  const [currentGuess, setCurrentGuess] = useState(''); // current guess being made
  const [gameWon, setGameWon] = useState(false);
  const [gameCompleted, setGameCompleted] = useState(false);
  const [isNewGame, setIsNewGame] = useState(false);
  const [invalidWord, setInvalidWord] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [game, setGame] = useState({
    game_id: '',
    username: '',
    guid: '',
    user_id: '',
    remain: 0,
    guesses: [],
    absent_letters: '',
    present_letters: '',
    correct_letters: '*****',
    completed: false,
    won: false,
    answer: '',
  });
  const mainRef = createRef(null);
  const inputRef = useRef(null);
  const [hasFocus, setHasFocus] = useState(true);
  const [hasError, setHasError] = useState(false);

  const clearLocalStorage = () => {
    localStorage.game_id = '';
    localStorage.guesses = '';
    localStorage.correct_letters = '*****';
    localStorage.absent_letters = '';
    localStorage.present_letters = '';
  }
  
  const fetchNewGame = (_username = username) => {
    clearLocalStorage();
    fetch(ORC_URL + '/game/new?username=' + _username,
      {
        method: 'POST',
      })
    .then(response => response.json())
    .then(data => {
      setGame({
        game_id: data.game_id,
        username: _username,
        guid: data.guid,
        user_id: data.user_id,
        remain: parseInt(data.remain),
        guesses: [],
        absent_letters: '',
        present_letters: '',
        correct_letters: '*****',
        completed: false,
        won: false,
      });
      localStorage.game_id = data.game_id;
    })
    .catch(err => {
      console.log(err);
      setHasError(true);
    })
  }

  const restoreFromLocalStorage = (async () => {
    /**
     * Restore game from DB using data from LocalStorage
     * return: true if game is found
     * false if game is not found
     */
    
    if (!localStorage.game_id){
      // console.log('failed to restore from local storage');
      // console.log('LocalStorage game_id: ' + localStorage.game_id);
      fetchNewGame(localStorage.username);
      return false;
    }
    // try to load unfinished game from Orc API using username and game_id from local storage
    // Orc API will call Play API to check if the game is still in Redis (gamme_id expires 24 hours after set in Redis)
    // we will also load present, absent, and correct letters from local storage
    // and guesses

    const res = await fetch(ORC_URL + '/game/restore?username=' + localStorage.username
    // const res = await fetch(endpoints[APP_SERVER]['orc'] + '/game/restore?username=' + localStorage.username
            + '&game_id=' + localStorage.game_id)

    .then(response => response.json())
    .then(data => {
      // console.log('Data from game/restore: ', data);
      // console.log('!data["result"]: ', !data['result']);
      if (!data['result']) { // No game found
        // console.log('Returning false from restoreFromLocalStorage');
        // console.log('failed to restore from local storage');
        // console.log('LocalStorage game_id: ' + localStorage.game_id);
        fetchNewGame(localStorage.username);
        return false;
      }
      else {  // unfinished game found
        // console.log('Returning true from restoreFromLocalStorage');
        let guesses = localStorage.guesses ? JSON.parse(localStorage.guesses) : [];
        setGuesses(guesses);
        setGuessIndex(guesses.length);
        setGame(() => ({
          ...game,
          game_id: data['game_id'],
          username: data['username'],
          guid: data['guid'],
          user_id: data['user_id'],
          remain: parseInt(data['remain']),
          guesses: guesses,
          absent_letters: localStorage.absent_letters,
          present_letters: localStorage.present_letters,
          correct_letters: localStorage.correct_letters,
        }));
        return true;
      }
    })
  })

  // first page load, start new game with username
  useEffect(() => {
    if (!username) {  // not necessary? username should be empty on first load 
      // if username is still in local storage, we might have an unfinished game
      if (localStorage.username) {
        setUsername(localStorage.username);
        // if we cannot restore from local storage, then fetch new game

        // NOTE: issue is this one is async and we have to await
        let restore_promise = restoreFromLocalStorage();
        // // will not work because we have to await for restorefromlocalStorage, but we cannot do that in useEffect because it is not async
        // console.log('restore_promise: ', (restore_promise));
        // // restore_promise.then(isRestored => {
        //   if (restore_promise)
        //     return;
        //   else {
        //     console.log('failed to restore from local storage');
        //     console.log('LocalStorage game_id: ' + localStorage.game_id);
        //     fetchNewGame(localStorage.username);
        //   }
        // // })

        // restoreFromLocalStorage().then(isRestored => { 
        //   console.log('isRestored: ', (isRestored));
        //   if (isRestored)
        //     return;
        //   else {
        //     console.log('failed to restore from local storage');
        //     console.log('LocalStorage game_id: ' + localStorage.game_id);
        //     fetchNewGame(localStorage.username);
        //   }
        // })
      }
      // otherwise prompt user to enter username
      else {
        setIsSettingUsername(true);
        return;
      }
    }


    mainRef.current.focus();      // focus on main on first page load
    // console.log('component did mount');
    window.scrollTo(-50, 0)
  }, [])

  // find a better way to detect when new username is entered 
  // only fetchNewGame for new username
  useEffect(() => {
    // done setting username
    if (!isSettingUsername && username !== '') {
      // if username is changed to a new one, then fetch new game
      // if (localStorage.username && localStorage.username !== username) {
        setGuesses([]);
        setGuessIndex(0);
        setCurrentGuess('');
        fetchNewGame();
      // }
      localStorage.username = username;
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
    if (!showAbout && !showStats && !showLeaderboard) {
      setTimeout(() => {
        inputRef.current.focus();
      }, 500);
    }
  }, [showAbout, showStats, showLeaderboard, hasError])

  const handleClick = () => {
    setGuesses([...guesses, GUESSES[guessIndex]]);
    setGuessIndex(guessIndex + 1);
  }

  // // debug only
  // useEffect(() => {
  //   console.log('useEffectgame: ', game);
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
      if (results[i] === 2) correct_letters += currentGuess[i];
      // if (results[i] === 2 && game.correct_letters[i] === '*') correct_letters += currentGuess[i];
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
    localStorage.correct_letters = correct_letters;
    localStorage.absent_letters = absent_letters;
    localStorage.present_letters = present_letters;
    localStorage.guesses = JSON.stringify([...guesses, currentGuess]);
    // if game is completed, return
    if (data['completed']) {
      setGameCompleted(true);
      clearLocalStorage();
      console.log('GAME COMPLETED: DID YOU WIN? ', data['won'])
      if (data['won']) {
        setGameWon(true); // for game completed dialog
      }
      return
    }
  }
  
  // refocus to next input after submitting a guess
  useEffect(() => {
    if (guessIndex < 6) // there will not be a 7th inputRef
      inputRef.current.focus();
      
    // setIsLoading(false);
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
        if (!isLoading) {
          
          setIsLoading(true);
          fetch(ORC_URL + '/game/' + game.game_id + '?username=' + username + '&guid=' + game.guid + '&user_id=' + game.user_id + '&guess=' + currentGuess,
          // fetch(endpoints[APP_SERVER]['orc'] + '/game/' + game.game_id + '?username=' + username + '&guid=' + game.guid + '&user_id=' + game.user_id + '&guess=' + currentGuess,
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
            // // start new game
            // if (data.completed)
            //   setGameCompleted(true);
            setIsLoading(false);
          })
          .catch(err => {
            console.log(err);
            setIsLoading(false);
            setHasError(true);
          })
          return;
        }
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
  
  return (
    <>
    {/* <h1 className='text-white'>VITE_DOMAIN_NAME: {new String(import.meta.env.VITE_DOMAIN_NAME)}</h1>
    <h1 className='text-white'>STATS_URL: {STATS_URL}</h1> */}
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
    {showAbout && 
      <AboutModal 
        setShowAbout={setShowAbout}
      />
    }
    {showStats && 
      <StatsDialog 
        setShowStats={setShowStats}
        username={username}
        user_id={game.user_id}
        // APP_SERVER={APP_SERVER}
        STATS_URL={STATS_URL}
        />
      }
    {showLeaderboard && 
      <LeaderboardModal 
        setShowLeaderboard={setShowLeaderboard}
        // APP_SERVER={APP_SERVER}
        STATS_URL={STATS_URL}
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
      setShowAbout={setShowAbout}
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
      <div className='flex flex-col items-center justify-center gap-2 pb-12'>
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
            ))}
          </div>
        ))}
      </div>
      
    </main>
    </>
  )
}

export default Wordle