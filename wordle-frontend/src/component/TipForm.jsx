import React from 'react';
import {useState, useEffect } from 'react';
import BillAmount from './BillAmount';
import TipAmount from './TipAmount';
import PeopleAmount from './PeopleAmount';

const TipForm = () => {
  const [bill, setBill] = useState(0);
  const [tip, setTip] = useState(0);
  const [people, setPeople] = useState(0);
  
  const [tipPerPerson, setTipPerPerson] = useState(0);
  const [totalPerPerson, setTotalPerPerson] = useState(0);
  const [total, setTotal] = useState(0);
  
  return (
    <form className='mx-auto grid max-w-6xl gap-y-5 lg:grid-cols-2 lg:gap-x-8'>
      <div className='flex flex-col gap-y-8 py-5 lg:px-5 lg:py-6'>
        <BillAmount bill={bill} setBill={setBill} />
        <TipAmount setTip={setTip}/>
        <PeopleAmount people={people} setPeople={setPeople}/>
      </div>
    </form>
  )
};

export default TipForm;