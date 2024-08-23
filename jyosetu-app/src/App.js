import './App.css';
import Sidebar from "./components/Sideber"
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './components/Home';
import Controller from './components/Controller';

function App() {
  return (
    <div className="App">
      <Router>
        <div className="main-container">
          <Sidebar />
          <div className='routes-container'>
            <Routes>
              <Route exact path="/" element={<Home />} />
              <Route path="/home" element={<Home />} />
              <Route path="/controller" element={<Controller />} />
            </Routes>
          </div>
        </div>
      </Router>      
    </div>
  );
}

export default App;
