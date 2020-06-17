import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min';
import React, { Component } from 'react';
import { Helmet } from 'react-helmet';

class Home extends Component {
    render() {
        return (
            <>
                <Helmet>
                    <title>Home - ToDo</title>
                </Helmet>
                <h1 className="text-center">Здравствуй, дорогой Пользователь!</h1>
                <div className="container">
                    <p className="text-centered">Это простой сайт для твоих задач. Здесь ты можешь легко <a href="/add">добавлять</a> свои задачи, <a href="/all">просматривать</a> их. Здесь есть классные фильтры, с которыми будет просто посмотреть свои задачи на <a href="/today">сегодня</a>, свои <a href="/overdue">просроченные</a> задачи, а также задачи на <a href="/pending">будущее</a>! Простым кликом по задаче ты можешь отметить что она выполнена, и так же просто отменить её выполнение.</p>
                </div>
            </>
        );
    };
}

export default Home
