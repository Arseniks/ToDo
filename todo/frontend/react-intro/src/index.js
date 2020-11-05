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
                    <Route exact path="/" component={Home} /> {/*See home.js for code for /home*/}
                    <Route exact path="/all" component={All} /> {/*See all.js for code for /all*/}
                    <Route exact path="/add" component={Add} /> {/*See add.js for code for /add*/}
                    <Route exact path="/today" component={Today} /> {/*See today.js for code for /today*/}
                    <Route exact path="/overdue" component={Overdue} /> {/*See overdue.js for code for /overdue*/}
                    <Route exact path="/pending" component={Pending} /> {/*See pending.js for code for /pending*/}
                </div>
            </BrowserRouter>
        </div>
    );
}


ReactDOM.render(<App />, document.getElementById('root'));
serviceWorker.register();
