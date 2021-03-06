/* Copyright 2012-2019 Ministerie van Sociale Zaken en Werkgelegenheid
 *
 * Licensed under the Apache License, Version 2.0 (the "License")
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import React from 'react';


class Menu extends React.Component {
    render() {
        if (this.props.hide) {
            return null;
        }
        return (
            <li className="nav-item dropdown mr-2">
                <a id={this.props.id} className="nav-link dropdown-toggle" role="button"
                   data-toggle="dropdown" href="#" aria-haspopup="true" aria-expanded="false">
                    {this.props.title}
                </a>
                <div className="dropdown-menu" aria-labelledby={this.props.id}>
                    {this.props.children}
                </div>
            </li>
        )
    }
}

class MenuItem extends React.Component {
    render() {
        if (this.props.hide) {
            return null;
        }
        var icon = this.props.check ? "✔ " : ""
        var disabled = this.props.disabled ? " disabled" : "";
        var propsClassName = this.props.className ? " " + this.props.className : "";
        var className = "dropdown-item" + disabled + propsClassName;
        return (
            <a className={className} id={this.props.id} href={"#" + this.props.href} onClick={this.props.onClick}
               data-toggle={this.props.data_toggle}>
                {icon + this.props.title}
            </a>
        );
    }
}


class NavItem extends React.Component {
    render () {
        if (this.props.hide) {
            return null;
        }
        var disabled = this.props.disabled ? " disabled" : "";
        var propsClassName = this.props.className ? " " + this.props.className : "";
        return (
            <li className="nav-item mr-2">
                <a className={"nav-link" + disabled + propsClassName} id={this.props.id}
                   href="#" onClick={this.props.onClick}>{this.props.title}</a>
            </li>
        );
    }
}

export {Menu, MenuItem, NavItem};
