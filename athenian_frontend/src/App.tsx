import React from 'react';
import logo from './logo.svg';
import './App.css';
import './components/main_view/MainView';
import MainView from './components/main_view/MainView';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="*" element={<MainView></MainView>}>
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
