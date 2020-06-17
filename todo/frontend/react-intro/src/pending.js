import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min';
import $ from 'jquery';
import React, { Component } from 'react';
import { Helmet } from 'react-helmet'
import Task from './task.js';

class Pending extends Component {
    state = {
        error: null,
        isLoaded: false,
        items: []
    };
    componentDidMount() {
        fetch("http://localhost:5000/pending/")
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
                        <Task item={item} key={item.uuid}/>
                    ))}
                    <p className="text-center">{items.length === 0 && "Нет заданий на будущее. Вы большой молодец!"}</p>
                </div>
            );
        }
    }
}

export default Pending;