import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min';
import $ from 'jquery';
import React, { Component } from 'react';
import { Helmet } from 'react-helmet'
import { v4 as uuid } from 'uuid';

class Add extends Component {
    constructor(props) {
        super(props);
        var d = new Date();
        this.state = {
            validate: false,
            name: "",
            descr: "",
            year: d.getFullYear(),
            month: d.getMonth(),
            day: d.getDay()
        };
    
        this.formSend = this.formSend.bind(this);
        this.chgName = this.chgName.bind(this);
        this.chgDescription = this.chgDescription.bind(this);
    }
    formSend(event) {
        event.preventDefault();
        this.setState({validate: true});
        var { name, descr, year, month, day} = this.state;
        if (name !== "" && descr !== "") {
            fetch("http://localhost:5000/add/", {method:"POST", body:JSON.stringify({"uuid":uuid(), "name":name, "description":descr, "date": year.toString() + '-' + month.toString() + '-' + day.toString(), "done": false})});
            document.location.href = "/all";
        }
    }

    chgName(event) {
        this.setState({name: event.target.value});
    }

    chgDescription(event) {
        this.setState({descr: event.target.value});
    }

    chgDate(event) {
        var arr = event.targer.value.split('.');
        this.setState({year: Number(arr[2]), month: Number(arr[1]), day: Number(arr[0])});
    }

    render() {
        $('#add').attr('class', 'nav-link disabled');
        var {validate} = this.state;
        return (
            <>
                <Helmet>
                    <title>Add - ToDo</title>
                </Helmet>
                <h1 className="text-center">Добавить задачу</h1>
                <div className="row justify-content-center">
                    <div className="col-md-6">
                        <form className={validate ? "was-validated" : ""} noValidate onSubmit={this.formSend}>
                            <div className="form-group">
                                <label htmlFor="name">Название</label>
                                <input type="text" className="form-control" id="name" onChange={this.chgName} required/>
                                <div className="invalid-feedback">
                                    Название не может быть пустым
                                </div>
                            </div>
                            <div className="form-group">
                                <label htmlFor="descr">Описание</label>
                                <textarea type="text" className="form-control" id="descr" onChange={this.chgDescription} required/>
                                <div className="invalid-feedback">
                                    Описание не может быть пустым
                                </div>
                            </div>
                            <div className="form-group">
                                <label htmlFor="descr">Срок выполнения</label>
                                <input type="date" className="form-control" required/>
                                <div className="invalid-feedback">
                                    Необходимо ввести срок выполнения
                                </div>
                            </div>
                            <button className="btn btn-primary" type="submit">Создать задачу</button>
                        </form>
                    </div>
                </div>
            </>
        );
    };
}

export default Add;