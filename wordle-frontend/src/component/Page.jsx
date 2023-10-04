import PanelLayout from "./PanelLayout";

import React from 'react';
import TipForm from "./TipForm";

const Page = () => {
  return (
    <main className=" flex min-h-screen flex-col items-center justify-center p-5 lg:p-24">
      <h1 className="my-14 text-center text-3xl font-bold uppercase tracking-widest text-cyan-800">
        Tip Splitter
      </h1>
      <PanelLayout>
        <TipForm/>
      </PanelLayout>
    </main>
  )
};

export default Page;