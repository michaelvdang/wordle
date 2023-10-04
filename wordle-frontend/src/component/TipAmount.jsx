import { useState } from "react";

const tips = [
  { tip: 5, isCustom: false },
  { tip: 10, isCustom: false },
  { tip: 15, isCustom: false },
  { tip: 20, isCustom: false },
  { tip: 25, isCustom: false },
  { tip: 30, isCustom: false },
  { tip: 0, isCustom: true },
]

import React from 'react'

const TipAmount = ({setTip}) => {
  const [customSelected, setCustomSelected] = useState(false);
  const [activeTip, setActiveTip] = useState(null);
  const [customTip, setCustomTip] = useState(0);
  
  return (
    <div>
      <label
        htmlFor="tip"
        className="block font-serif text-sm font-light leading-6 text-gray-600"
      >
        Select Tip in %
      </label>

      <div className="mt-2 grid grid-cols-3 gap-3">
        {tips.map((tip, index) => (
          <div key={index}>
            {tip.isCustome ? (
              <>
                {customSelected ? (
                  <input
                    type="number"
                    id="tip"
                    name="tip"
                    className="block h-full w-full rounded-md border-0 px-2 py-1.5
                    text-gray-900 outline-none ring-1 ring-inset ring-gray-300 
                    placeholder:text-gray-400 focus:ring-2 focus:ring-inset
                    focus:ring-cyan-500 sm:text-sm sm:leading-6"
                    placeholder="0.00"
                    aria-describedby="tip-amount"
                    value={customTip}
                    onChange={(e) => setCustomTip(e.target.value)}
                  />
                ): (
                  <button
                    type="button"
                    className="w-full rounded-md bg-gray-100 px-3.5 py-2.5 font-medium
                    text-cyan-700 shadow-sm hover:bg-gray-200 focus-visible:outline
                    focus-visible:outline-2 focus-visible:outline-offset-2
                    focus-visible:outline-cyan-600"
                  >
                    Custom
                  </button>
                )}
              </>
            ) : (
              <button
              type="button"
              className={`${
                activeTip === tip.tip
                  ? 'bg-cyan-200 text-cyan-700 hover:bg-cyan-100'
                  : 'bg-cyan-600 text-white hover:bg-cyan-500'
              } w-full rounded-md px-3.5 py-2.5 file:font-medium
              shadow-sm focus-visible:outline
              focus-visible:outline-2 focus-visible:outline-offset-2
              focus-visible:outline-cyan-600`} 
              >
                {tip.tip}%
              </button>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

export default TipAmount