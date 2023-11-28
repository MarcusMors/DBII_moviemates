// Copyright (C) 2022 José Enrique Vilca Campana
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as
// published by the Free Software Foundation, either version 3 of the
// License, or (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Affero General Public License for more details.
//
// You should have received a copy of the GNU Affero General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.

const API = "http://localhost:5000/api/"

let insert_guide_element = document.getElementById("insert_guide")

function get_data() {
	let request = API + "rand_movies"
	fetch(request, {
		method: "POST",
		body: JSON.stringify({}),
		headers: { "content-type": "application/json; charset=UTF-8" },
	}).then(function (response) {
			return response.json()
		})
		.then(function (response) {
			let movies = response["movies"]

			for (const movie of movies) {
				let anchor_container = document.createElement("a")
				let div_container = document.createElement("div")
				anchor_container.append(div_container)
				anchor_container.setAttribute("class", "product-ref")
				div_container.setAttribute("class", "product-container")

				let product_title = document.createElement("p")
				let product_plot = document.createElement("p")
				let product_year = document.createElement("p")
				let product_poster = document.createElement("img")
				div_container.append(
					product_year,
					product_plot,
					product_title,
					product_poster
				)

				product_title.append(movie["title"])
				product_plot.append(movie["plot"])
				product_year.append(movie["year"])

				product_poster.setAttribute("src", movie["poster"])

				insert_guide_element?.appendChild(anchor_container)
			}
		})
}



/**
 * @param {{ textContent: string; }} t_error_message_element
 * @param {string} t_error_message
 */
function set_error_message(t_error_message_element, t_error_message) {
	t_error_message_element.textContent = ""
	t_error_message_element.textContent = t_error_message
}

const t_threshold = 0.10

function handler(entries) {
	// const entry = entries[0]
	// const is_visible = entry.intersectionRation >= t_threshold
	// console.log(entry)
	// if (is_visible) {
	console.log("IS FUCKING VISIBLE")
	get_data()
}

let signal_element = document.getElementById("load_signal")
const config = { threshold: t_threshold }
const observer = new IntersectionObserver(handler, config)
observer.observe(signal_element)
