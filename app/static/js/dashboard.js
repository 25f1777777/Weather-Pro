let currentCity = "";

const searchBtn =
document.getElementById("searchBtn");

const cityInput =
document.getElementById("cityInput");

const addFavoriteBtn =
document.getElementById("addFavoriteBtn");

const loadingSpinner =
document.getElementById("loadingSpinner");

const currentWeatherCard =
document.getElementById("currentWeatherCard");

const aqiCard =
document.getElementById("aqiCard");

const forecastCard =
document.getElementById("forecastCard");

const forecastContainer =
document.getElementById("forecastContainer");



searchBtn.addEventListener(
    "click",
    searchWeather
);

cityInput.addEventListener(
    "keypress",
    (e) => {

        if (e.key === "Enter") {
            searchWeather();
        }

    }
);

addFavoriteBtn.addEventListener(
    "click",
    addFavorite
);



function showToast(
    message,
    type = "success"
) {

    const toast = document.createElement(
        "div"
    );

    toast.className =
        `custom-toast ${type}`;

    toast.innerText = message;

    document.body.appendChild(
        toast
    );

    setTimeout(() => {

        toast.classList.add(
            "show"
        );

    }, 100);

    setTimeout(() => {

        toast.remove();

    }, 3000);

}



async function searchWeather() {

    const city =
        cityInput.value.trim();

    if (!city) {

        showToast(
            "Please enter a city.",
            "error"
        );

        return;
    }

    currentCity = city;

    showLoading();

    try {

        const response =
            await fetch(
                `/api/weather?city=${encodeURIComponent(city)}`
            );

        const data =
            await response.json();

        hideLoading();

        if (!data.success) {

            showToast(
                data.message,
                "error"
            );

            return;
        }

        populateCurrentWeather(
            data.current
        );

        populateAQI(
            data.air_quality
        );

        populateForecast(
            data.forecast
        );

        localStorage.setItem(
            "lastCity",
            city
        );

        showToast(
            `${city} loaded successfully`
        );

    }

    catch (error) {

        console.error(error);

        hideLoading();

        showToast(
            "Unable to fetch weather.",
            "error"
        );

    }

}


function showLoading() {

    loadingSpinner.classList.remove(
        "d-none"
    );

}

function hideLoading() {

    loadingSpinner.classList.add(
        "d-none"
    );

}


function populateCurrentWeather(
    weather
) {

    currentWeatherCard.classList.remove(
        "d-none"
    );

    document.getElementById(
        "cityName"
    ).textContent =
        weather.name;

    document.getElementById(
        "weatherDescription"
    ).textContent =
        weather.weather[0].description;

    document.getElementById(
        "temperature"
    ).textContent =
        `${Math.round(
            weather.main.temp
        )}°C`;

    document.getElementById(
        "humidity"
    ).textContent =
        `${weather.main.humidity}%`;

    document.getElementById(
        "windSpeed"
    ).textContent =
        `${weather.wind.speed} m/s`;

    document.getElementById(
        "pressure"
    ).textContent =
        `${weather.main.pressure} hPa`;

    document.getElementById(
        "feelsLike"
    ).textContent =
        `${Math.round(
            weather.main.feels_like
        )}°C`;

    const icon =
        weather.weather[0].icon;

    document.getElementById(
        "weatherIcon"
    ).src =
        `https://openweathermap.org/img/wn/${icon}@4x.png`;

}



function populateAQI(
    aqiData
) {

    aqiCard.classList.remove(
        "d-none"
    );

    const aqi =
        aqiData.list[0].main.aqi;

    const labels = {

        1: "Good 🌱",
        2: "Fair 🙂",
        3: "Moderate 😐",
        4: "Poor 😷",
        5: "Very Poor ☠️"

    };

    document.getElementById(
        "aqiValue"
    ).textContent =
        labels[aqi];

}



function populateForecast(
    forecast
) {

    forecastCard.classList.remove(
        "d-none"
    );

    forecastContainer.innerHTML =
        "";

    const daily =
        forecast.list.filter(
            item =>
            item.dt_txt.includes(
                "12:00:00"
            )
        );

    daily.forEach(day => {

        const icon =
            day.weather[0].icon;

        const html = `

        <div class="col-lg-2 col-md-4 col-6 mb-3">

            <div class="forecast-box">

                <h6>
                    ${new Date(
                        day.dt_txt
                    ).toLocaleDateString(
                        "en-US",
                        {
                            weekday:
                            "short"
                        }
                    )}
                </h6>

                <img
                src="https://openweathermap.org/img/wn/${icon}@2x.png">

                <h5>
                    ${Math.round(
                        day.main.temp
                    )}°C
                </h5>

            </div>

        </div>

        `;

        forecastContainer.insertAdjacentHTML(
            "beforeend",
            html
        );

    });

}



async function addFavorite() {

    if (!currentCity) {

        showToast(
            "Search a city first.",
            "error"
        );

        return;
    }

    try {

        const formData =
            new FormData();

        formData.append(
            "city",
            currentCity
        );

        const response =
            await fetch(
                "/favorites/add",
                {
                    method: "POST",
                    body: formData
                }
            );

        const data =
            await response.json();

        if (data.success) {

            showToast(
                "Added to favorites"
            );

            setTimeout(() => {

                location.reload();

            }, 1000);

        }

        else {

            showToast(
                data.message ||
                "Already exists",
                "error"
            );

        }

    }

    catch (error) {

        console.error(error);

        showToast(
            "Failed to add favorite",
            "error"
        );

    }

}



document.addEventListener(
    "click",
    async (e) => {

        const btn =
            e.target.closest(
                ".delete-favorite"
            );

        if (!btn) return;

        const id =
            btn.dataset.id;

        try {

            const response =
                await fetch(
                    `/favorites/delete/${id}`,
                    {
                        method: "DELETE"
                    }
                );

            const result =
                await response.json();

            if (result.success) {

                showToast(
                    "Favorite removed"
                );

                setTimeout(() => {

                    location.reload();

                }, 800);

            }

        }

        catch (error) {

            console.error(error);

        }

    }
);



document.addEventListener(
    "click",
    (e) => {

        const city =
            e.target.closest(
                ".favorite-city span"
            );

        if (!city) return;

        cityInput.value =
            city.innerText;

        searchWeather();

    }
);


window.addEventListener(
    "load",
    () => {

        if (
            cityInput.value.trim()
        ) {
            return;
        }

        const city =
            localStorage.getItem(
                "lastCity"
            );

        if (city) {

            cityInput.value = city;

        }

    }
);




document.addEventListener(
    "DOMContentLoaded",
    () => {

        const cityInput =
            document.getElementById(
                "cityInput"
            );

        if (
            cityInput &&
            cityInput.value.trim()
        ) {

            fetchWeather(
                cityInput.value.trim()
            );

        }

    }
);



document.addEventListener(
    "DOMContentLoaded",
    () => {

        const cityInput =
            document.getElementById(
                "cityInput"
            );

        const city =
            cityInput.value.trim();

        if (city) {

            document
                .getElementById(
                    "searchBtn"
                )
                .click();

        }

    }
);