import { Fragment, useRef, useState } from 'react'
import { Dialog, Transition } from '@headlessui/react'
import { ExclamationTriangleIcon } from '@heroicons/react/24/outline'
import {UserIcon} from '@heroicons/react/20/solid';

export default function UsernameDialog(props) {
  const {username, setUsername, setIsSettingUsername, mainRef} = props;
  const [newUsername, setNewUsername] = useState(username);
  const [open, setOpen] = useState(true);
  const [alert, setAlert] = useState(false);  // red letter under input field

  const inputUsernameRef = useRef(null)

  const handleSetUsername = () => {
    setUsername(newUsername);
    setIsSettingUsername(false);
    // mainRef.current.focus();
  }

  const handleCancel = () => {
    if (newUsername === '') {
      setAlert(true);
    } else {
      setIsSettingUsername(false);
      // mainRef.current.focus();
    }
  }
  
  const handleClosing = () => {
    setShowStats(false);
    // mainRef.current.focus();
  }

  return (
    <>
    {!open && 
      <button onClick={() => setOpen(!open)} className="fixed inset-0 z-10 bg-red-500">
        hi 
      </button>
      
    }
    
    <Transition.Root show={open} as={Fragment}>
      <Dialog as="div" className="relative z-10" initialFocus={inputUsernameRef} onClose={handleCancel}>
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
          <div className="flex min-h-full items-center justify-center p-4 text-center sm:items-center sm:p-0">
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
                    <div className="mx-auto flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-full bg-slate-200 sm:mx-0 sm:h-10 sm:w-10">
                      <UserIcon className='h-5 w-5 text-gray-400' aria-hidden='true' />
                      {/* <ExclamationTriangleIcon className="h-6 w-6 text-red-600" aria-hidden="true" /> */}
                    </div>
                    <div className="flex-grow mt-3 text-center sm:ml-4 sm:mt-0 sm:text-left">
                      <Dialog.Title as="h3" className="text-base font-semibold leading-6 text-gray-200">
                        Pick a username
                      </Dialog.Title>
                      <div className="mt-4">
                        {/* <p className="text-sm text-gray-500">
                          Are you sure you want to deactivate your account? All of your data will be permanently
                          removed. This action cannot be undone.
                        </p> */}
                        <div className='relative mt-2 flex flex-grow items-stretch focus-within:z-10'>
                          {/* <div className='absolute pointer-events-none inset-y-0 left-0 flex items-center pl-3'>
                            <UserIcon className='h-5 w-5 text-gray-400' aria-hidden='true' />
                          </div> */}
                          <input
                            type='text'
                            name='username'
                            id='username'
                            autoComplete='username'
                            autoCapitalize='none'
                            className='block w-full rounded-md border-0 py-1.5 pl-3 pr-3 font-serif
                            text-gray-500 outline-none ring-1 ring-inset ring-gray-300
                            placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-cyan-500
                            sm:text-sm sm:leading-6'
                            placeholder='username'
                            aria-describedby='number-of-people'
                            value={newUsername}
                            ref={inputUsernameRef}
                            onChange={(e) => {setNewUsername(e.target.value)}}
                            onKeyDown={(e) => {
                              if (e.key === 'Enter') handleSetUsername();
                            }}
                          />
                        </div>
                      </div>
                      {alert && (
                        <div className='text-red-500 text-sm'>
                          Must set a username
                        </div>
                      )}
                    </div>
                  </div>
                </div>
                <div className="px-4 py-3 sm:flex sm:flex-row justify-center gap-x-4">
                  <button
                    type="button"
                    className="inline-flex w-full justify-center rounded-md bg-green-400 px-3 py-2 
                      text-sm font-semibold text-slate-900 shadow-sm hover:bg-green-500 hover:text-white
                      sm:ml-3 sm:w-auto"
                    onClick={handleSetUsername}
                  >
                    Set Username
                  </button>
                  <button
                    type="button"
                    className="mt-3 inline-flex w-full justify-center rounded-md bg-white px-3 py-2 
                    text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 
                    hover:bg-gray-50 sm:mt-0 sm:w-auto"
                    onClick={handleCancel}
                  >
                    Cancel
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
