import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min';
import $ from 'jquery';
import React, { Component } from 'react';
import { Helmet } from 'react-helmet'
import Task from './task.js';
import { EmojiSmile } from 'react-bootstrap-icons';
import * as config from './config.json';

class Pending extends Component {
    state = {
        error: null,
        isLoaded: false,
        items: []
    };
    componentDidMount() {
        var host = config.backend.host;
        var port = config.backend.port;
        fetch(`http://${host}:${port}/pending/`)
            .then(res => res.json())
            .then(
                (result) => {
                    this.setState({ items: result, isLoaded: true });
                },
                (error) => {
                    this.setState({
                        isLoaded: true,
                        error: error
                    });
                }
            );
    }
    render() {
        $('#pending').attr('class', 'nav-link disabled');
        const { error, isLoaded, items } = this.state;
        if (error) {
            return <div>Ошибка: {error.message}</div>;
        } else if (!isLoaded) {
            return <div>Загрузка...</div>;
        } else {
            return (
                <div className="container">
                    <Helmet>
                        <title>Pending - ToDo</title>
                    </Helmet>
                    <h1 className="text-center">Задания на будущее</h1> 
                    {items.map((item) => (
                        <Task item={item} key={item.uuid} delete={true}/>
                    ))}
                    <p className="text-center">{items.length === 0 && "Нет заданий на будущее. Ты большой молодец!"} {items.length === 0 && <EmojiSmile/>}</p>
                </div>
            );
        }
    }
}

export default Pending;