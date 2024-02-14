import { Fragment, useEffect, useState } from 'react'
import { Dialog, Transition } from '@headlessui/react'

export default function AboutModal(props) {
  const {setShowAbout} = props;

  const [open, setOpen] = useState(true);


  const handleClosing = () => {
    setShowAbout(false);
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
                    {/* <div className='flex items-center justify-center'>
                      <div className="mx-auto flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-full bg-slate-200 sm:mx-0 sm:h-10 sm:w-10">
                        <UserIcon className='h-5 w-5 text-gray-400' aria-hidden='true' />
                      </div>
                    </div> */}
                    <div className="flex-grow text-center">
                      <Dialog.Title as="h3" className="text-base font-semibold leading-6 text-gray-200">
                        About this app
                      </Dialog.Title>
                    </div>
                  </div>
                  <div className="px-4">
                    <div className="sm:flex sm:items-start">
                      <div className="w-full ">
                        <div className='relative mt-2 flex flex-col flex-grow items-stretch focus-within:z-10'>
                          {/** table */}
                          <div className="flex flex-col  overflow-x-auto sm:-mx-6 lg:-mx-8  min-w-full py-2 sm:px-6 lg:px-8  text-gray-200">
                            <div className="overflow-hidden">
                              <p>This app was made for educational purposes only.</p>
                              <p>Technologies used:</p>
                              <p>&#8269; Front end:</p>
                              <p>&nbsp;&nbsp;&#8227; React - Tailwind</p>
                              <p>&#8269; Back end:</p>
                              <p>&nbsp;&nbsp;&#8227; FastAPI - Redis - SQLite</p>
                              <p>&nbsp;&nbsp;&nbsp;&nbsp;&#8226; Redis for active game and leaderboard data</p>
                              <p>&nbsp;&nbsp;&nbsp;&nbsp;&#8226; SQLite for user data, game results, game data, and word bank</p>
                              <p>&nbsp;&nbsp;&nbsp;&nbsp;&#8226; 
                                FastAPI for microservices including stats, word check, word validation, game play, orchestrator</p>
                            </div>
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
                    onClick={() => setShowAbout(false)}
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
