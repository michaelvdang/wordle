import React from 'react'

const DisplayCard = (props) => {
  const {tipPerPerson, totalPerPerson, total, reset} = props;
  const data = [
    {
      label: 'Tip Amount',
      value: tipPerPerson.toFixed(2),
    },
    {
      label: 'Total',
      value: totalPerPerson.toFixed(2),
    },
  ]

  return (
    <div className='flex flex-col justify-between rounded-xl bg-cyan-700 p-5 lg:py-10'>
      <div className='flex flex-col gap-y-8'>
        {data.map((item, i) => (
          <div key={i} className='flex items-end justify-between'>
            <div>
              <p className='font-serif text-white lg:text-lg'>{item.label}</p>
              <p className='font-serif text-xs font-light text-gray-300 lg:text-sm'>
                / person
              </p>
            </div>
            <div className='flex items-baseline gap-x-2'>
              <span className='text-xl font-extralight text-white lg:text-xl'>
                $
              </span>
              <span className='font-serif text-3xl font-medium text-white lg:text-4xl'>
                {item.value}
              </span>
            </div>
          </div>
        ))}
      </div>

    </div>
  )
}

export default DisplayCard