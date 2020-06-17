import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min'
import React, { Component } from 'react';
import { XCircle, CheckCircle } from 'react-bootstrap-icons';

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
        done: this.props.item.done
    };

    taskClick(id) {
        this.setState((state) => ({done:!state.done}));
        fetch('http://localhost:5000/toggle/', {method:'PATCH', body:JSON.stringify({'uuid':id})});
        document.location.reload();
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
            <div id={item.uuid + 'ts'} className={cls.concat(color)} onClick={this.taskClick.bind(this, item.uuid)}>
                <div className="row">
                    <div className="col-4">
                        <h5>{item.name}</h5>
                    </div>
                    <div className="col-8 row">
                        <p className="col-10">{item.description}</p>
                        <p className="col-2 text-right" id={item.uuid + 'gl'}><Glyph done={this.state.done} /></p>
                    </div>
                </div>
            </div>
        )
    }
} 

export default Task;
