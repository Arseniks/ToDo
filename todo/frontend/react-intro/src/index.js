import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min'
import React, { Component } from 'react';
import { BrowserRouter, Route } from "react-router-dom";
import { Helmet } from 'react-helmet'
import ReactDOM from 'react-dom';
import * as serviceWorker from './serviceWorker';
import All from './all.js';
import Add from './add.js'
class Home extends Component {
    render() {
        return (
        <>
            <Helmet>
                <title>Home - ToDo</title>
            </Helmet>
            <h1 className="text-center">Здравствуй, дорогой Пользователь!</h1>
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
                </div>
            </BrowserRouter>
        </div>
    );
}


ReactDOM.render(<App />, document.getElementById('root'));
serviceWorker.register();
