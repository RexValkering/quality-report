/* Copyright 2012-2017 Ministerie van Sociale Zaken en Werkgelegenheid
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


function create_dashboard_table(dashboard) {
    var table = ['<div id="section_dashboard"><table class="table table-condensed table-bordered dashboard"><thead>',
                 '<tr style="color: white; font-weight: bold; background-color: #2F95CF">'];
    dashboard["headers"].forEach(function(cell) {
        table.push('<th colspan=' + cell["colspan"] + ' style="text-align: center;">' + cell["header"] + '</th>');
    });
    table.push('</th></thead><tbody>');
    dashboard["rows"].forEach(function(row) {
        table.push('<tr>');
        row.forEach(function(cell) {
            table.push('<td colspan=' + cell['colspan'] + ' rowspan=' + cell['rowspan'] + ' bgcolor="' +
                       cell['bgcolor'] + '">');
            table.push('<div class="piechart_div"><canvas class="piechart_canvas" id="section_summary_chart_' + cell['section_id'] + '"></canvas></div></td>');
        });
        table.push('</tr>');
    });
    table.push('</tbody></table>');
    return table.join('');
}

function dashboard_columns(dashboard) {
    var nr_columns = 0;
    dashboard["headers"].forEach(function(cell) {
        nr_columns += cell["colspan"];
    });
    return nr_columns;
}

function dashboard_rows(dashboard) {
    return 1 + dashboard["rows"].length;
}

export {create_dashboard_table, dashboard_columns, dashboard_rows};
