import { Fragment, useEffect, useState } from 'react'
import { Dialog, Transition } from '@headlessui/react'
import { ExclamationTriangleIcon } from '@heroicons/react/24/outline'
import {UserIcon} from '@heroicons/react/20/solid';

const stats = {
  user_id: 'User ID',
  username: 'Username',
  games_won: 'Games Won',
  games_played: 'Games Played',
  win_percentage: 'Win Percentage',
  average_guesses: 'Average Guesses',
  current_streak: 'Current Streak',
  max_win_streak: 'Max Streak',
}

export default function StatsDialog(props) {
  const {setShowStats, username, user_id, inputRef} = props;
  const [userStats, setUserStats] = useState({
    win_percentage: '',
    // user_id,
    // username,
    games_played: 0,
    games_won: 0,
    average_guesses: 0,
    current_streak: 0,
    max_win_streak: 0,
  })
  const [open, setOpen] = useState(true);

  useEffect(() => {
    // console.log('usename: ', username);
    // console.log('user_id: ', user_id);
    // console.log(`http://localhost:9000/stats/users?user_id=` + user_id + '&username=' + username);
    // fetch(`http://mikespace.xyz:9000/stats/users?user_id=` + user_id + '&username=' + username)
    // fetch(`http://localhost:9000/stats/users?user_id=` + user_id + '&username=' + username)
    fetch(`https://stats.api.mikespace.xyz/stats/users?user_id=` + user_id + '&username=' + username)
      .then(res => res.json())
      .then(res => {
        // console.log(res);
        setUserStats({
          win_percentage: (res.win_percentage ? (res.win_percentage * 100).toFixed(2).toString() + '%' : '0.00%'),
          games_played: res.games_played,
          games_won: res.games_won,
          average_guesses: (res.average_guesses ? res.average_guesses.toFixed(2) : 'N/A'),
          current_streak: res.current_streak 
            ?  (res.current_streak.streak + (res.current_streak.won ? ' Wins' : ' Losses'))
            : 'N/A',
          max_win_streak: res.max_win_streak,
          // win_percentage: (res.win_percentage ? (res.win_percentage * 100).toFixed(2).toString() + '%' : 'N/A'),
          // // user_id: user_id,
          // // username: username,
          // games_played: res.games_played,
          // games_won: res.games_won,
          // average_guesses: (res.average_guesses ? res.average_guesses.toFixed(2) : 'N/A'),
          // current_streak: res.current_streak 
          //     ?  (res.current_streak.streak + (res.current_streak.won ? 'W' : 'L'))
          //     : 'N/A',
          // max_win_streak: res.max_win_streak ? res.max_win_streak : 'N/A',
        })
      })
    return () => {
      // console.log('component will unmount');
      // inputRef.current.focus();
    }
  }, []);

  const handleClosing = () => {
    setShowStats(false);
    // mainRef.current.focus();
    // inputRef.current.focus();
  }

  return (
    <>
    <Transition.Root show={true} as={Fragment}>
      <Dialog as="div" className="relative z-10" onClose={handleClosing}>
        <Transition.Child
          as={Fragment}
          enter="ease-out duration-300"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="ease-in duration-200"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" />
        </Transition.Child>

        <div className="fixed inset-0 z-10 w-screen overflow-y-auto">
          <div className="flex min-h-full items-center justify-center p-4 text-center sm:p-0">
            <Transition.Child
              as={Fragment}
              enter="ease-out duration-300"
              enterFrom="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
              enterTo="opacity-100 translate-y-0 sm:scale-100"
              leave="ease-in duration-200"
              leaveFrom="opacity-100 translate-y-0 sm:scale-100"
              leaveTo="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
            >
              <Dialog.Panel className="relative transform overflow-hidden rounded-lg bg-gray-600 
                text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg">
                <div className="px-4 pb-4 pt-5 sm:p-6 sm:pb-4">
                  <div className="sm:flex sm:items-start">
                    <div className='flex items-center justify-center'>
                      <div className="mx-auto flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-full bg-slate-200 sm:mx-0 sm:h-10 sm:w-10">
                        <UserIcon className='h-5 w-5 text-gray-400' aria-hidden='true' />
                        {/* <ExclamationTriangleIcon className="h-6 w-6 text-red-600" aria-hidden="true" /> */}
                      </div>
                    </div>
                    <div className="flex-grow mt-3 text-center sm:ml-4 sm:mt-0 sm:text-left">
                      <Dialog.Title as="h3" className="text-base font-semibold leading-6 text-gray-200">
                        {username}
                      </Dialog.Title>
                    </div>
                  </div>
                  <div className="px-4">
                    <div className="sm:flex sm:items-start">
                      <div className="w-full ">
                        <div className='relative mt-2 flex flex-col flex-grow items-stretch focus-within:z-10'>
                          {/** table */}
                          <div className="flex flex-col  overflow-x-auto sm:-mx-6 lg:-mx-8  min-w-full py-2 sm:px-6 lg:px-8">
                            {/* <div className="overflow-x-auto sm:-mx-6 lg:-mx-8">
                              <div className="inline-block min-w-full py-2 sm:px-6 lg:px-8"> */}
                                <div className="overflow-hidden">
                                  <table className="min-w-full text-left text-sm font-light">
                                    {/* <thead
                                      class="border-b bg-white font-medium dark:border-neutral-500 dark:bg-neutral-600">
                                      <tr>
                                        <th scope="col" class="px-6 py-4">#</th>
                                        <th scope="col" class="px-6 py-4">First</th>
                                        <th scope="col" class="px-6 py-4">Last</th>
                                        <th scope="col" class="px-6 py-4">Handle</th>
                                      </tr>
                                    </thead> */}
                                    <tbody>
                                      {Object.keys(userStats).map((key, index) => {
                                        return (
                                          <tr key={index}
                                            className="border-b text-gray-200 bg-gray-600  dark:border-neutral-500 dark:bg-gray-600">
                                            <td className="whitespace-nowrap px-6 py-4">{stats[key]}</td>
                                            <td className="whitespace-nowrap px-6 py-4">
                                              {userStats[key]}
                                              {/* {userStats[key]
                                                ? userStats[key]
                                                : 'N/A'} */}
                                            </td>
                                          </tr>
                                        )
                                      })}
                                      {/* <tr
                                        class="border-b bg-neutral-100 dark:border-neutral-500 dark:bg-neutral-700">
                                        <td class="whitespace-nowrap px-6 py-4">Win Percentage</td>
                                        <td class="whitespace-nowrap px-6 py-4">{userStats.win_percentage}%</td>
                                      </tr>
                                      <tr
                                        class="border-b bg-neutral-100 dark:border-neutral-500 dark:bg-neutral-700">
                                        <td
                                          colspan="2"
                                          class="whitespace-nowrap px-6 py-4 text-center">
                                          Larry the Bird
                                        </td>
                                      </tr> */}
                                    </tbody>
                                  </table>
                                </div>
                              {/* </div>
                            </div> */}
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div className="px-4 py-3 sm:flex sm:flex-row justify-center gap-x-4">
                  <button
                    type="button"
                    className="mt-3 inline-flex w-full justify-center rounded-md bg-white px-3 py-2 
                    text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 
                    hover:bg-gray-50 sm:mt-0 sm:w-auto"
                    onClick={() => setShowStats(false)}
                  >
                    Close
                  </button>
                </div>
              </Dialog.Panel>
            </Transition.Child>
          </div>
        </div>
      </Dialog>
    </Transition.Root>
    </>
  )
}
