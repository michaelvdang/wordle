import Page from "./component/Page";
import React from "react";

export default function App() {
  // const data = fetch('http://localhost:8000/')
  // const data = fetch('https://jsonplaceholder.typicode.com/todos/1')

  // // testing the API
  const data = fetch('http://146.190.58.25:9400/')
      .then(response => response.json())
      .then(data => console.log(data))
  
  // // // add new guess
  // const guid = "afd0b036-625a-3aa8-b639-9dc8c8fff0ff";
  // const game_id = 1519;
  // const guess = "cloud";
  // const data = fetch('http://146.190.58.25:9400/game/' + game_id 
  //     + '?guid=' + guid + '&guess=' + guess,
  //   {
  //     method: 'POST',
  //   })
  //       .then(response => response.json())
  //       .then(data => console.log(data))
        
  // // start new game
  // const data = fetch('http://146.190.58.25:9400/game/new?user_name=ucohen',
  //   {
  //     method: 'POST',
  //   })
  //       .then(response => response.json())
  //       .then(data => console.log(data))
  
  return (
    <Page/>

    // <main className="flex min-h-screen flex-col items-center justify-center p-5 lg:p-24">
    //   <h1 className="my-14 text-center text-3xl font-bold uppercase tracking-widest text-cyan-800">
    //     Tip Splitter
    //   </h1>
    //   <PanelLayout></PanelLayout>
    // </main>
  )
};