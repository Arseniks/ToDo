import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min'
import React from 'react';
import { BrowserRouter, Route } from "react-router-dom";
import ReactDOM from 'react-dom';
import * as serviceWorker from './serviceWorker';
import All from './all.js';
import Add from './add.js';
import Today from './today.js';
import Overdue from './overdue.js';
import Pending from './pending.js';
import Home from './home.js';

function App() {
    return (
        <div className="App">
            <BrowserRouter>
                <div>
                    <Route exact path="/" component={Home} />
                    <Route exact path="/all" component={All} />
                    <Route exact path="/add" component={Add} />
                    <Route exact path="/today" component={Today} />
                    <Route exact path="/overdue" component={Overdue} />
                    <Route exact path="/pending" component={Pending} />
                </div>
            </BrowserRouter>
        </div>
    );
}


ReactDOM.render(<App />, document.getElementById('root'));
serviceWorker.register();
