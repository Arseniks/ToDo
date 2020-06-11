import 'bootstrap/dist/css/bootstrap.min.css';
import $ from 'jquery';
import Popper from 'popper.js';
import 'bootstrap/dist/js/bootstrap.bundle.min'
import React, { Component } from 'react';
import { BrowserRouter, Route } from "react-router-dom";
import { Helmet } from 'react-helmet'
import ReactDOM from 'react-dom';
import * as serviceWorker from './serviceWorker';

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
                    <Route exact path="/hello" component={Home} />
                </div>
            </BrowserRouter>
        </div>
    );
}


ReactDOM.render(<App />, document.getElementById('root'));
serviceWorker.register();
