// src/App.tsx

import React from 'react';
import './App.css';
import { useWallet, InputTransactionData } from "@aptos-labs/wallet-adapter-react";
import { Aptos } from "@aptos-labs/ts-sdk";
import { connected } from 'process';
import { PetraWallet } from "petra-plugin-wallet-adapter";
import { WalletSelector } from "@aptos-labs/wallet-adapter-ant-design";
import "@aptos-labs/wallet-adapter-ant-design/dist/index.css";


const App: React.FC = () => {

  const { account, signAndSubmitTransaction, connect } = useWallet();
  const aptos = new Aptos();
  const moduleAddress = "0x750e3394f4551dcf9d61b5152260ddf6c0cdf781064874bb27a66c330072d31d";
 
  // Display account address after successful connection
  if (account) {
    console.log("User address:", account.address);
  }
  // TypeScript function to be called on button click
  const handleClick = async () => {
    console.log('Button clicked!'); // You can replace this with any logic you want;
    console.log(account?.address);
    await fnnn();
  };

  const fnnn = async () => {
    if (!account) return [];
  
     const transaction:InputTransactionData = {
        data: {
          function:`${moduleAddress}::DeNuVModule::initialize_platform`,
          functionArguments:[]
        }
      }
    try {
      // sign and submit transaction to chain
      const response = await signAndSubmitTransaction(transaction);
      // wait for transaction
      await aptos.waitForTransaction({transactionHash:response.hash});
      console.log(response, response.hash);
    } catch (error: any) {
      console.log(error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>React TypeScript Button Example</h1>
        
        {/* Button that calls the handleClick function */}
        <button onClick={handleClick}>
          Click Me!
        </button>
        
  <WalletSelector />

      </header>
    </div>
  );
};

export default App;
