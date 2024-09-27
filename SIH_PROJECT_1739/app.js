// This function calculates the solar position (azimuth and elevation)
// for a given date, time, latitude, and longitude.
function calculateSolarPosition(date, latitude, longitude) {
    // Convert date to Julian date
    const julianDate = toJulianDate(date);

    // Number of centuries since J2000.0
    const T = (julianDate - 2451545.0) / 36525.0;

    // Calculate solar coordinates
    const solarCoords = getSolarCoordinates(T);

    // Local sidereal time in degrees
    const LST = getLocalSiderealTime(date, longitude);

    // Hour angle of the Sun in degrees
    const hourAngle = LST - solarCoords.rightAscension;

    // Convert latitude to radians
    const latitudeRad = toRadians(latitude);

    // Calculate the elevation angle
    const elevation = Math.asin(
        Math.sin(latitudeRad) * Math.sin(toRadians(solarCoords.declination)) +
        Math.cos(latitudeRad) * Math.cos(toRadians(solarCoords.declination)) * Math.cos(toRadians(hourAngle))
    );

    // Calculate the azimuth angle
    const azimuth = Math.atan2(
        -Math.sin(toRadians(hourAngle)),
        Math.tan(toRadians(solarCoords.declination)) * Math.cos(latitudeRad) -
        Math.sin(latitudeRad) * Math.cos(toRadians(hourAngle))
    );

    return {
        elevation: toDegrees(elevation), // Convert elevation from radians to degrees
        azimuth: (toDegrees(azimuth) + 360) % 360 // Convert azimuth from radians to degrees and normalize
    };
}

// Helper function to convert a date to Julian date
function toJulianDate(date) {
    return (date / 86400000) + 2440587.5;
}

// Helper function to convert degrees to radians
function toRadians(degrees) {
    return degrees * Math.PI / 180;
}

// Helper function to convert radians to degrees
function toDegrees(radians) {
    return radians * 180 / Math.PI;
}

// Calculate the right ascension and declination of the Sun
function getSolarCoordinates(T) {
    // Mean anomaly of the Sun in degrees
    const M = (357.5291 + 35999.0503 * T) % 360;

    // Mean longitude of the Sun in degrees
    const L0 = (280.46646 + 36000.76983 * T) % 360;

    // Ecliptic longitude of the Sun in degrees
    const lambda = L0 + (1.914602 - 0.004817 * T - 0.000014 * T * T) * Math.sin(toRadians(M)) +
        (0.019993 - 0.000101 * T) * Math.sin(toRadians(2 * M)) +
        0.000289 * Math.sin(toRadians(3 * M));

    // Obliquity of the ecliptic in degrees
    const epsilon = 23.439 - 0.0000004 * T;

    // Right ascension of the Sun in degrees
    const rightAscension = toDegrees(Math.atan2(Math.cos(toRadians(epsilon)) * Math.sin(toRadians(lambda)), Math.cos(toRadians(lambda))));

    // Declination of the Sun in degrees
    const declination = toDegrees(Math.asin(Math.sin(toRadians(epsilon)) * Math.sin(toRadians(lambda))));

    return { rightAscension, declination };
}

// Calculate the local sidereal time
function getLocalSiderealTime(date, longitude) {
    const jd = toJulianDate(date);
    const T = (jd - 2451545.0) / 36525.0;
    const GMST = 280.46061837 + 360.98564736629 * (jd - 2451545) + T * T * (0.000387933 - T / 38710000);
    return (GMST + longitude) % 360;
}

// Example usage:
// Example of a specific date and time input:
// Let's say you want to calculate for September 25, 2024, at 15:30 UTC
const y = 2023;
const m = 8;
const d = 1;

const date = new Date(Date.UTC(y, m, 1, 15, 30)); // Months are 0-based, so 8 is September
const latitude = 40.7128; // Example: Latitude for New York City
const longitude = -74.0060; // Example: Longitude for New York City


const solarPosition = calculateSolarPosition(date, latitude, longitude);
console.log(`Azimuth: ${solarPosition.azimuth.toFixed(2)} degrees`);
console.log(`Elevation: ${solarPosition.elevation.toFixed(2)} degrees`);
