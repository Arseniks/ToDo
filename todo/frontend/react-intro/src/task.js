import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min';
import $ from 'jquery';
import React, { Component } from 'react';
import { XCircle, CheckCircle } from 'react-bootstrap-icons';
import * as config from './config.json';

function Glyph(props) {
    var { done , id } = props;
    if (done) {
        return (<CheckCircle size={40} id={id}/>);
    } else {
        return (<XCircle size={40} id={id}/>);
    }
}
class Task extends Component {
    state = {
        done: this.props.item.done,
        delete: this.props.delete
    };

    taskClick(id, delet) {
        this.setState((state) => ({done:!state.done}));
        var host = config.backend.host;
        var port = config.backend.port;
        fetch(`http://${host}:${port}/toggle/`, {method:'PATCH', body:JSON.stringify({'uuid':id})});
        if (delet) {
            $('#' + id + 'ts').remove();
            if ($('p').text() === ' ' || $('p').text() === '') {
                document.location.reload();
            }
        }
    }

    getDate(date) {
        var dt = new Date(date);
        return dt.toLocaleString('ru', {
            weekday: "short",
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    }
    componentDidUpdate() {
        if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
            $(".m-3").toggleClass("m-3").toggleClass("my-3");
        }
    }
    componentDidMount() {
        if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
            $(".m-3").toggleClass("m-3").toggleClass("my-3");
        }
    }

    render() {
        var {item} = this.props;
        var color;
        if (this.state.done) {
            color = 'success';
        } else {
            color = 'danger';
        }
        var cls = 'container rounded border m-3 p-3 bg-';
        return (
            <div id={item.uuid + 'ts'} className={cls.concat(color)} onClick={this.taskClick.bind(this, item.uuid, this.state.delete)}>
                <div className="row">
                    <div className="col-3">
                        <h5 className="text-break">{item.name}</h5>
                    </div>
                    <div className="col-9 row">
                        <p className="col-7 text-break">{item.description}</p>
                        <p className="col-3 p-0">{this.getDate(item.date)}</p>
                        <p className="col-2 text-right" id={item.uuid + 'gl'}><Glyph done={this.state.done} /></p>
                    </div>
                </div>
            </div>
        )
    }
} 

export default Task;
