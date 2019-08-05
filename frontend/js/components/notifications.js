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

            let report_date_time = new Date(this.props.report_date_time[0], this.props.report_date_time[1] - 1,
                                            this.props.report_date_time[2], this.props.report_date_time[3],
                                            this.props.report_date_time[4])
            var now = new Date();
            var seconds = parseInt((now - report_date_time)/1000, 10);

            // Add a warning if the report hasn't run for 26 hours.
            if (seconds > 60 * 60 * 26) {
                messages.push(
                    <div className="alert alert-warning" role="alert">De scan is afgelopen nacht niet met succes afgerond. Bekijk de logbestanden op de server voor meer informatie.</div>
                );
            }

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
