import { Fragment, useEffect, useState } from 'react'
import { Dialog, Transition } from '@headlessui/react'
import { ExclamationTriangleIcon } from '@heroicons/react/24/outline'
import {UserIcon} from '@heroicons/react/20/solid';
import TopStreaksTable from './TopStreaksTable';
import TopWinsTable from './TopWinsTable';

const stats = {
  user_id: 'User ID',
  username: 'Username',
  games_won: 'Games Won',
  games_played: 'Games Played',
  win_percentage: 'Win Percentage',
  average_guesses: 'Average Guesses',
  current_streak: 'Current Streak',
  max_streak: 'Max Streak',
}

export default function LeaderboardModal(props) {
  const {setShowLeaderboard} = props;
  const [topStreaks, setTopStreaks] = useState([])
  const [topWins, setTopWins] = useState([])
  const [viewTopWins, setViewTopWins] = useState(true);
  const [open, setOpen] = useState(true);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    // fetch(`http://mikespace.xyz:9000/stats/top_streaks_and_winners`)
    fetch(`http://localhost:9000/stats/top_streaks_and_winners`)
      .then(res => res.json())
      .then(res => {
        // console.log(res);
        setTopStreaks(res.top_streaks);
        setTopWins(res.top_wins);
        setLoading(false);
      })
  }, [])
  
  const handleClosing = () => {
    setShowLeaderboard(false);
  }

  // all the below used the template in the StatsDialog
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
                    <div className="flex-grow mt-3 text-center sm:ml-4 sm:mt-0 sm:text-left">
                      <Dialog.Title as="h3" className="text-base font-semibold leading-6 text-gray-200">
                        {viewTopWins ? 'Top Wins' : 'Top Streaks'}
                      </Dialog.Title>
                    </div>
                  </div>

                  {viewTopWins ? (
                    (topWins.length 
                      ? <TopWinsTable topWins={topWins} loading={loading} /> 
                      : <div className='px-4'>Data not available</div>
                    )
                  ) : (
                    (topStreaks.length
                      ? <TopStreaksTable topStreaks={topStreaks} loading={loading} /> 
                      : <div className='px-4'>Data not available</div>
                    )
                  )}
                </div>
                <div className="px-4 py-3 sm:flex sm:flex-row justify-center gap-x-4">
                  {viewTopWins ? (
                    <button
                      type="button"
                      className="mt-3 inline-flex w-full justify-center rounded-md bg-white px-3 py-2 
                      text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 
                      hover:bg-gray-50 sm:mt-0 sm:w-auto"
                      onClick={() => setViewTopWins(!viewTopWins)}
                    >
                      View Top Streaks
                    </button>
                  ) : (
                    <button
                      type="button"
                      className="mt-3 inline-flex w-full justify-center rounded-md bg-white px-3 py-2 
                      text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 
                      hover:bg-gray-50 sm:mt-0 sm:w-auto"
                      onClick={() => setViewTopWins(!viewTopWins)}
                    >
                      View Top Wins
                    </button>
                  )}
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
