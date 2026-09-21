"""Weather station analyzer.

Reads station temperature observations from a file, computes per-station
statistics, finds stations whose latest reading is above their mean, and
writes formatted statistics back out to a file.
"""

import datetime
import os
import sys
import tempfile
import unittest
from typing import Dict, List, Tuple

DATE_FORMAT = "%I:%M:%S %p %m/%d/%Y"
MIN_VALID_TEMP = -100.0
MAX_VALID_TEMP = 150.0

Observation = Tuple[datetime.datetime, float]
Observations = Dict[str, List[Observation]]
Statistics = Dict[str, Dict[str, float]]


def read_observations(filename: str) -> Tuple[Observations, List[Tuple[int, str]]]:
    """Read station observations from a file.

    Each line in the file must have the format "station,date,temperature",
    where date is formatted like "09:28:09 AM 04/20/2026" and temperature
    is a float in the range [-100.0, 150.0].

    :param filename: path to the observations file
    :return: a tuple (observations, errors) where observations maps each
        station name to a list of (date, temperature) tuples sorted by
        date, and errors is a list of (line_number, error_message) tuples
        describing malformed lines, invalid temperatures, and duplicate
        station/date combinations
    :raises OSError: re-raised if the file cannot be opened
    """
    observations: Observations = {}
    errors: List[Tuple[int, str]] = []
    seen: set = set()

    try:
        file = open(filename, "r")
    except OSError as error:
        print(f"Could not open file '{filename}': {error}")
        raise

    with file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()
            if not line:
                continue

            parts = line.split(",")
            if len(parts) != 3:
                errors.append((line_number, f"Malformed line: '{line}'"))
                continue

            station, date_text, temperature_text = (part.strip() for part in parts)

            try:
                date = datetime.datetime.strptime(date_text, DATE_FORMAT)
            except ValueError:
                errors.append((line_number, f"Invalid date: '{date_text}'"))
                continue

            try:
                temperature = float(temperature_text)
            except ValueError:
                errors.append((line_number, f"Invalid temperature: '{temperature_text}'"))
                continue

            if not (MIN_VALID_TEMP <= temperature <= MAX_VALID_TEMP):
                errors.append((line_number, f"Temperature out of range: {temperature}"))
                continue

            key = (station, date)
            if key in seen:
                errors.append(
                    (line_number, f"Duplicate observation for '{station}' at {date}")
                )
                continue
            seen.add(key)

            observations.setdefault(station, []).append((date, temperature))

    for station_observations in observations.values():
        station_observations.sort(key=lambda observation: observation[0])

    return observations, errors


def station_statistics(observations: Observations) -> Statistics:
    """Compute min, max, and mean temperature for each station.

    :param observations: dict mapping station name to a list of
        (date, temperature) tuples
    :return: dict mapping each station to a dict with keys "min", "max",
        and "mean", each a float
    """
    statistics: Statistics = {}
    for station, station_observations in observations.items():
        temperatures = [temperature for _, temperature in station_observations]
        statistics[station] = {
            "min": min(temperatures),
            "max": max(temperatures),
            "mean": sum(temperatures) / len(temperatures),
        }
    return statistics


def station_outliers(
    observations: Observations,
) -> Dict[str, Tuple[datetime.datetime, float, float]]:
    """Find stations whose latest temperature reading exceeds their mean.

    :param observations: dict mapping station name to a list of
        (date, temperature) tuples
    :return: dict mapping station name to (latest_date, latest_temperature,
        mean_temperature) for every station whose latest reported
        temperature is greater than its mean temperature
    """
    statistics = station_statistics(observations)
    return {
        station: (station_observations[-1][0], station_observations[-1][1], statistics[station]["mean"])
        for station, station_observations in observations.items()
        if station_observations[-1][1] > statistics[station]["mean"]
    }


def write_statistics(filename: str, statistics: Statistics) -> None:
    """Write station statistics to a file in alphabetical order by station.

    Each numeric value is written with exactly one digit after the
    decimal point.

    :param filename: path to the output file
    :param statistics: dict mapping station name to a dict with keys
        "min", "max", and "mean"
    :return: None
    """
    with open(filename, "w") as file:
        for station in sorted(statistics):
            values = statistics[station]
            file.write(
                f"{station},min={values['min']:.1f},"
                f"max={values['max']:.1f},mean={values['mean']:.1f}\n"
            )


class WeatherStationAnalyzerTests(unittest.TestCase):
    """Tests for the weather station analyzer functions."""

    def setUp(self) -> None:
        """Create a temporary directory to hold test input/output files."""
        self._temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self) -> None:
        """Clean up the temporary directory created in setUp."""
        self._temp_dir.cleanup()

    def _write_temp_file(self, contents: str) -> str:
        """Write contents to a temp file and return its path."""
        path = os.path.join(self._temp_dir.name, "observations.csv")
        with open(path, "w") as file:
            file.write(contents)
        return path

    def test_multiple_stations_with_valid_data(self) -> None:
        """Observations for multiple stations are parsed and grouped correctly."""
        contents = (
            "StationA,09:00:00 AM 04/20/2026,70.0\n"
            "StationB,10:00:00 AM 04/20/2026,55.0\n"
            "StationA,11:00:00 AM 04/20/2026,75.0\n"
        )
        path = self._write_temp_file(contents)

        observations, errors = read_observations(path)

        self.assertEqual(errors, [])
        self.assertEqual(set(observations.keys()), {"StationA", "StationB"})
        self.assertEqual(len(observations["StationA"]), 2)
        self.assertEqual(len(observations["StationB"]), 1)

    def test_negative_temperatures(self) -> None:
        """Valid negative temperatures within range are accepted."""
        contents = "StationA,09:00:00 AM 04/20/2026,-40.5\n"
        path = self._write_temp_file(contents)

        observations, errors = read_observations(path)

        self.assertEqual(errors, [])
        self.assertEqual(observations["StationA"][0][1], -40.5)

    def test_duplicate_station_date_rejected(self) -> None:
        """A duplicate station/date combination is recorded as an error."""
        contents = (
            "StationA,09:00:00 AM 04/20/2026,70.0\n"
            "StationA,09:00:00 AM 04/20/2026,71.0\n"
        )
        path = self._write_temp_file(contents)

        observations, errors = read_observations(path)

        self.assertEqual(len(observations["StationA"]), 1)
        self.assertEqual(len(errors), 1)
        self.assertIn("Duplicate", errors[0][1])

    def test_temperature_out_of_range_rejected(self) -> None:
        """Temperatures outside [-100.0, 150.0] are rejected with an error."""
        contents = (
            "StationA,09:00:00 AM 04/20/2026,200.0\n"
            "StationA,10:00:00 AM 04/20/2026,-150.0\n"
            "StationA,11:00:00 AM 04/20/2026,50.0\n"
        )
        path = self._write_temp_file(contents)

        observations, errors = read_observations(path)

        self.assertEqual(len(observations["StationA"]), 1)
        self.assertEqual(len(errors), 2)
        self.assertTrue(all("out of range" in message for _, message in errors))

    def test_station_statistics_min_max_mean(self) -> None:
        """station_statistics correctly computes min, max, and mean."""
        contents = (
            "StationA,09:00:00 AM 04/20/2026,10.0\n"
            "StationA,10:00:00 AM 04/20/2026,20.0\n"
            "StationA,11:00:00 AM 04/20/2026,30.0\n"
        )
        path = self._write_temp_file(contents)
        observations, _ = read_observations(path)

        statistics = station_statistics(observations)

        self.assertEqual(statistics["StationA"]["min"], 10.0)
        self.assertEqual(statistics["StationA"]["max"], 30.0)
        self.assertEqual(statistics["StationA"]["mean"], 20.0)

    def test_write_statistics_alphabetical_order_and_formatting(self) -> None:
        """write_statistics writes stations alphabetically with one decimal digit."""
        statistics = {
            "StationC": {"min": 1.0, "max": 2.0, "mean": 1.5},
            "StationA": {"min": 10.25, "max": 20.75, "mean": 15.333},
            "StationB": {"min": 5.0, "max": 5.0, "mean": 5.0},
        }
        output_path = os.path.join(self._temp_dir.name, "stats.csv")

        write_statistics(output_path, statistics)

        with open(output_path) as file:
            lines = file.readlines()

        stations_in_order = [line.split(",")[0] for line in lines]
        self.assertEqual(stations_in_order, ["StationA", "StationB", "StationC"])
        self.assertIn("min=10.2", lines[0])
        self.assertIn("mean=15.3", lines[0])

    def test_observations_sorted_by_date(self) -> None:
        """Observations for a station are sorted chronologically by date."""
        contents = (
            "StationA,11:00:00 AM 04/20/2026,30.0\n"
            "StationA,09:00:00 AM 04/20/2026,10.0\n"
            "StationA,10:00:00 AM 04/20/2026,20.0\n"
        )
        path = self._write_temp_file(contents)

        observations, _ = read_observations(path)
        dates = [date for date, _ in observations["StationA"]]

        self.assertEqual(dates, sorted(dates))

    def test_read_observations_missing_file_raises(self) -> None:
        """read_observations re-raises when the file cannot be opened."""
        missing_path = os.path.join(self._temp_dir.name, "does_not_exist.csv")

        with self.assertRaises(FileNotFoundError):
            read_observations(missing_path)


def main() -> None:
    """Run the weather station analyzer as a command-line program.

    Reads the input filename from sys.argv[1] and the output filename
    from sys.argv[2], reports observation errors, prints station
    statistics and outliers, and writes statistics to the output file.

    :return: None
    """
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    try:
        observations, errors = read_observations(input_filename)
    except (FileNotFoundError, PermissionError, OSError) as error:
        print(f"Unable to process '{input_filename}': {error}")
        sys.exit(1)

    if errors:
        print("Errors encountered while reading observations:")
        for line_number, message in errors:
            print(f"  Line {line_number}: {message}")
    else:
        print("No errors encountered while reading observations.")

    statistics = station_statistics(observations)
    print("\nStation statistics:")
    for station in sorted(statistics):
        values = statistics[station]
        print(
            f"  {station}: min={values['min']:.1f}, "
            f"max={values['max']:.1f}, mean={values['mean']:.1f}"
        )

    outliers = station_outliers(observations)
    print("\nStation outliers (latest temperature above mean):")
    for station in sorted(outliers):
        date, temperature, mean = outliers[station]
        print(f"  {station}: {temperature:.1f} at {date} (mean={mean:.1f})")

    write_statistics(output_filename, statistics)


if __name__ == "__main__":
    main()
