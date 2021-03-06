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

import test from 'tape';
import {TrendGraphs} from '../js/components/trend_graphs.js';

test('parse history should create JS Dates', function(t) {
    t.deepEqual(TrendGraphs.parse_history_json([[[2016, 10, 27, 22, 5, 49], [3, 0, 2, 0, 0, 0, 135]]]),
                [[new Date(2016, 10, 27, 22, 5, 49)], [3], [0], [2], [0], [0], [0], [135]]);
    t.end();
});

test('parse history should create datasets', function(t) {
    t.deepEqual(TrendGraphs.parse_history_json([[[2016, 10, 27, 22, 5, 49], [3, 0, 2, 0, 0, 0, 135]],
                                    [[2016, 10, 28, 9, 0, 0], [3, 0, 3, 1, 1, 1, 5]]]),
                [[new Date(2016, 10, 27, 22, 5, 49), new Date(2016, 10, 28, 9, 0, 0)],
                 [3, 3], [0, 0], [2, 3], [0, 1], [0, 1], [0, 1], [135, 5]]);
    t.end();
});
