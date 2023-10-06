import React, {createRef, useEffect, useState} from 'react'

const LETTERS = [
  ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
  ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
  ['Z', 'X', 'C', 'V', 'B', 'N', 'M']
]

const KEYS = [
  [0,1,2,3,4],[5,6,7,8,9],[10,11,12,13,14],[15,16,17,18,19],[20,21,22,23,24],
]

const GUESSES = [
  'angry', 'happy', 'cloud', 'viper', 'sheer'
]

const Wordle = () => {
  const [guesses, setGuesses] = useState([]);       // array of made guesses
  const [guessIndex, setGuessIndex] = useState(0);  // index of the current guess
  // const [letterIndex, setLetterIndex] = useState(0);
  const [currentGuess, setCurrentGuess] = useState(''); // current guess being made
  const mainRef = createRef(null);
  
  const handleClick = () => {
    setGuesses([...guesses, GUESSES[guessIndex]]);
    setGuessIndex(guessIndex + 1);
  }

  // useEffect(() => {
  //   document.addEventListener('keydown', handleKeyDown)
  //   return () => {
  //     document.removeEventListener('keydown', null);
  //   }
  // }, [])

  useEffect(() => {
    console.log('useEffect currentGuess: ', currentGuess);
    mainRef.current.focus();
    return () => {
    }
  }, [guesses, currentGuess])
  
  
  const handleKeyDown = (e) => {
    if (guesses.length > 5) return;
    if (e.key === 'Backspace') {
      setCurrentGuess(currentGuess.slice(0, -1));
      return;
    }
    if (currentGuess.length > 4) {
      if (e.key === 'Enter') {
        setGuesses(() => [...guesses, currentGuess]);
        setGuessIndex(guessIndex + 1);
        setCurrentGuess('');
        return;
      }
      return;
    }
    if (e.keyCode >= 65 && e.keyCode <= 90) {
      setCurrentGuess(currentGuess => currentGuess + e.key);
    }

  }

  const bubbleStyle = 'flex items-center justify-center bg-white \
                        rounded-full cursor-default select-none text-gray-800 w-28 h-28 \
                        font-bold text-6xl pb-1 font-serif';
  
  return (

    <main 
      className="flex min-h-screen flex-col items-center justify-center p-5 outline-none" 
      onKeyDown={handleKeyDown}
      tabIndex={0}
      ref={mainRef}
    >
      <div className='grid grid-rows-5 gap-2 mb-24'>
        {[0,1,2,3,4].map((i) => (
          <div key={i} className='grid grid-cols-5 gap-2'>
            {guesses[i] 
              // if rendering past guesses
              ? guesses[i].split('').map((letter, index) => (
                  <div key={KEYS[i][index]} className={bubbleStyle} onClick={handleClick}>
                    {letter ? letter : ' '}
                  </div>
                ))
              // else: if rendering current guess
              : (currentGuess && guessIndex === i)
                ? (currentGuess.length === 5)      
                  // highlight all five characters if there are 5 letters in currentGuess
                  ? currentGuess.split('').map((letter, index) => (
                      <div key={KEYS[i][index]} 
                        className={`${bubbleStyle}
                        shadow-[0_0_5px_7px_rgba(0,0,0,0.3)] shadow-gray-500`} // find the column to highlight the incoming letter of current guess
                        onClick={handleClick}>
                        {letter}
                      </div> 
                      )) 
                  // otherwise only highlight incoming letter
                  : currentGuess.padEnd(5, ' ').split('').map((letter, index) => (
                  <div key={KEYS[i][index]} 
                    className={`${bubbleStyle} 
                    ${index === currentGuess.length 
                      ? 'shadow-[0_0_5px_7px_rgba(0,0,0,0.3)] shadow-gray-500' 
                      : ''}` } // find the column to highlight the incoming letter of current guess
                    onClick={handleClick}>
                    {letter}
                  </div> 
                  ))
                // else: not current guess, rendering blank spaces
                : '     '.split('').map((space, index) => (
                  <div key={KEYS[i][index]} 
                    className={`${bubbleStyle} 
                    ${i === guesses.length && index === 0
                      ? 'shadow-[0_0_5px_7px_rgba(0,0,0,0.3)] shadow-gray-500'
                      : ''}`}
                    onClick={handleClick}>
                    {space}
                  </div>
                  ))

              
            }
          </div>
        ))}
      </div>
      <div className='flex flex-col items-center justify-center gap-2'>
        {LETTERS.map((row) => (
          <div key={row} className='flex flex-row gap-1'>
            {row.map((i) => (
              <div key={i} className='flex items-center justify-center bg-white 
              cursor-default select-none rounded-3xl
              text-gray-800 w-10 h-10 font-bold text-sm pb-1 font-serif'>
                {i}
              </div>
            ))}
          </div>
        ))}
      </div>
      
    </main>
  )
}

export default Wordle