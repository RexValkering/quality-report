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


class Notifications extends React.Component {

    constructor() {
        super();
        this.state = {notifications: 'loading'};
    }

    componentDidMount() {
        var self = this;
        $.getJSON("json/notifications.json", "", function(notifications) {
            self.setState((state) => ({notifications: notifications}));
        });
    }

    render() {
        if (this.state.notifications === 'loading') {
            return null;
        } else {
            let messages = [];
            this.state.notifications.forEach(function(notification, index) {
                let classes = 'alert alert-' + notification.type
                messages.push(
                    <div className={classes} role="alert">{notification.message}</div>
                );
            }, this);
            return (
                <div>
                    {messages}
                </div>
            );
        }
    }
}

export {Notifications};
