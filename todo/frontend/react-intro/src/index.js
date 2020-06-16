import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min'
import React, { Component } from 'react';
import { BrowserRouter, Route } from "react-router-dom";
import { Helmet } from 'react-helmet'
import ReactDOM from 'react-dom';
import * as serviceWorker from './serviceWorker';
import All from './all.js';
import Add from './add.js';
import Today from './today.js';

class Home extends Component {
    render() {
        return (
            <>
                <Helmet>
                    <title>Home - ToDo</title>
                </Helmet>
                <h1 className="text-center">Здравствуй, дорогой Пользователь!</h1>
                <a href="/all">To All tasks</a>
                <a href="/add">To Add tasks</a>
            </>
        );
    };
}

function App() {
    return (
        <div className="App">
            <BrowserRouter>
                <div>
                    <Route exact path="/" component={Home} />
                    <Route exact path="/all" component={All} />
                    <Route exact path="/add" component={Add} />
                    <Route exact path="/today" component={Today} />
                </div>
            </BrowserRouter>
        </div>
    );
}


ReactDOM.render(<App />, document.getElementById('root'));
serviceWorker.register();
