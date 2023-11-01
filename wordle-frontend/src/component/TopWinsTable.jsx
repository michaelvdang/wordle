import React from 'react'

const TopWinsTable = (props) => {
  const {topWins, loading} = props;
  
  return (
    <>
    <div className="px-4">
      <div className="sm:flex sm:items-start">
        <div className="w-full ">
          <div className='relative mt-2 flex flex-col flex-grow items-stretch focus-within:z-10'>
            {loading ? (
              <div>Loading...</div>
            ) : (
              // table
              <div className="flex flex-col  overflow-x-auto sm:-mx-6 lg:-mx-8  min-w-full py-2 sm:px-6 lg:px-8">
                <div className="overflow-hidden">
                  <table className="min-w-full text-left text-sm font-light table-fixed">
                    <tbody>
                      {topWins.map((user, index) => {
                        return (
                          <tr key={index}
                            className="border-b bg-gray-600  dark:border-neutral-500 dark:bg-gray-600">
                            <td className="whitespace-nowrap px-6 py-4 w-3/4">{user[0]}</td>
                            <td className="whitespace-nowrap px-6 py-4 w-1/4">
                              {user[1]}
                            </td>
                          </tr>
                        )
                      })}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
    </>
  )
}

export default TopWinsTable