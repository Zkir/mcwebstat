

This project consists of a set of Python scripts that generate a (almost) static website displaying player statistics for a Minecraft server. 

The scripts read data directly from the Minecraft server files, process it, and generate HTML, JSON, and image files. The generated website includes player statistics, activity graphs, and medals.



### Prerequisites

Install the required Python dependencies:

```bash
pip install -r requirements.txt
```

### Configuration

1.  Create a `mcwebstat_config.yml` file in the root directory of the project.
2.  Add the following content to the file, replacing `d:/.minecraft_server` with the actual path to your Minecraft server directory:

```yaml
MINECRAFT_DIR: d:/.minecraft_server
```

### Generating Statistics

The following batch scripts are provided to update the statistics:

*   `update_player_stat.bat`: This script generates the main player statistics, converts markdown documentation to HTML, creates a site map, and generates player medals. It then copies the generated files to the web server root.
*   `update_player_activity.bat`: This script generates player activity graphs and copies them to the web server root.

To run the scripts, simply execute the batch files from the command line.

**Note:** The batch scripts contain a hardcoded web server root directory (`d:\_minecraft_site`). You may need to edit these files to match your environment.
