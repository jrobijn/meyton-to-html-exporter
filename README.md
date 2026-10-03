# Meyton Results To HTML Exporter

This repository contains a utility script to export competition results from Meyton's electronic shooting range system database into static HTML files. These files can be generated ad-hoc for intermediate results and displayed on monitors during a competition.

The script queries a Meyton database for the series results of a given date and generates **one HTML file per discipline**. Each page shows, per participant: name, club, score per series, inner tens and total score. Participants are ranked by total score (with inner tens as a tie-breaker).

The generated pages are plain, self-contained HTML with inline CSS and no JavaScript, so they load instantly and render consistently on any display. The logo is embedded directly into each page, so the HTML files are fully portable.

By default the exporter writes the HTML files into an `output` folder in the current working directory, which is created if it doesn't exist. All of the mentioned behaviour can be customized using CLI parameters.

## Configuration

The script has to have certain environment variables configured and can optionally be further configured using certain CLI parameters.

### Environment variables

In order to run the script several environment variables need to be set to configure the correct MariaDB credentials and connection information. The following environment variables are configurable (and most are assumed to be there):

| Environment variable | Default | Description                                                                |
| -------------------- | --------| -------------------------------------------------------------------------- |
| MARIADB_USER         |         | The user to use for authentication to the MariaDB server                   |
| MARIADB_PASSWORD     |         | The password to use for authentication to the MariaDB server               |
| MARIADB_HOST         |         | The IP address at which the MariaDB endpoint is located                    |
| MARIADB_PORT         | 3306    | The port number through which the MariaDB endpoint can be accessed         |
| MARIADB_DATABASE     |         | The name of the database in the MariaDB server that should be connected to |

### Command line interface parameters

The execution of the script can be optionally customized using the following CLI parameters:

| Command line parameter | Default                 | Description                                                                                 |
| ---------------------- | ----------------------- | ------------------------------------------------------------------------------------------- |
| date                   | *Today*                 | The competition date for which results should be collected and exported (format YYYY-MM-DD) |
| output-folder          | output                  | The output folder to which the generated HTML files should be saved                         |
| template-file          | input/template.html     | Path to the HTML page template filled in for each discipline                                |
| logo-file              | assets/logo-white.png   | Path to a logo image embedded into each HTML page (pass a non-existent path to omit it)     |

Each generated file is named `<discipline>-<date>.html` (e.g. `air-rifle-10m-2026-03-21.html`).

The HTML page template lives in `input/template.html` and can be freely edited. It uses `$`-prefixed placeholders that are filled in at generation time: `$discipline`, `$date`, `$logo` and `$rows` (the ranked table rows).


## Local environment execution

It's possible to run the script locally provided you have direct access to the MariaDB endpoint.

### Preparation

First install Python 3.14 (might work with lower versions but untested). Optionally set up a virtual environment. After this the necessary Python packages can be installed using pip by running the following command in the repository root:
```sh
pip install -r requirements.txt
```

All of the necessary environment variables can be set in a `.env` file in the root of the repository. The `.env` file should have the following format:

```
MARIADB_USER=
MARIADB_PASSWORD=
MARIADB_HOST=
MARIADB_PORT=
MARIADB_DATABASE=
```

### Execution

The script can be executed using the following command from the repository root:
```sh
python exporter/main.py
```

The above mentioned CLI parameters can also be added to customize the script behaviour. For example:
```sh
python exporter/main.py --date 2026-03-21 --output-folder output
```

Because the HTML files are generated ad-hoc, you can simply re-run the script during a competition to refresh the intermediate results shown on the monitors.

## Docker image execution

The script can also be run in a Docker container. This has the benefit of using a self-contained environment that's easily reproducable in a cross-platform way

### Preparation

First install Docker. After this you can build the Docker image using the following command in the repository root:
```sh
docker build -t meyton-to-html-exporter:<tag> .
```

Also create a `docker.env` file that will contain environment variable values with the required MariaDB configuration (see earlier section for an example). You can skip this if you want to pass the environment variables separately using the `--env` CLI parameter for the `docker run` command.

Make sure you have an `output` folder available to which the generated HTML files can be written.

It's also possible to run the Docker container from anywhere on your machine, but you have to make sure the output subdirectory is available

### Execution

The Docker container (based on the built image) can be run using the following command, if run from the repository root (with created `output` folder and `docker.env` environment variables file):
```sh
docker run --env-file docker.env --volume $(pwd)/output:/home/appuser/app/output meyton-to-html-exporter:local
```

This will mount the `output` subdirectory in the Docker container and run the script, such that the generated HTML files will appear in the `output` directory.

It's also possible to pass CLI parameters to the script by appending them to the `docker run` invocation. For example:
```sh
docker run --env-file docker.env --volume $(pwd)/output:/home/appuser/app/output meyton-to-html-exporter:local --date 2026-01-31
```

Like mentioned earlier it's also possible to use `--env` flags instead of `--env-file` with a environment variable file. And it's possible to run the container anywhere on the system so long as the image was built. Adjust the volume mounts accordingly if you do that.
