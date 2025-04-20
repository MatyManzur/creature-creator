# Home Assignment 3
**Subject**: Application or use cases of various design patterns
**Students**:
- Mauro Leandro Baez
- Matias Manzur
**Lecturer**: Maxim Glaida
**Date**: 20/04/2025

## What is this?
We decided to make a sims-like character creator, but instead of creating humans, you create animal mixes! It's as weird as it sounds... The animals themselves are made in 32 bits artstyle, so it might be a good idea to not maximize the window.

## How to run

**Requirements**: 
- `python3.10` or higher
- `pip`
- Docker

In order to run our project, just execute `install.sh` (or `install.bat` in Windows) in order to create a virtual environment and install the dependencies (Pillow & tk).

Then you can start the LLM server with Docker.
`docker pull mauritobaez/design_patterns_assignment:latest`
`docker run --rm -it -p 11434:11434 mauritobaez/design_patterns_assignment`

Finally, in another terminal you can just run `./run.sh` (or `run.bat` in Windows).

**Note:** If by any reason pip is unable to install tkinter, and your system's python installation does not include it by default, you may need to install it with something like `sudo apt install python3-tk`. It is a package used for generating the GUI.

To run tests you can execute `./test.sh` in Linux.

## Design Patterns Applied (Third Assignment)
The 3 design patterns chosen are: **Proxy LLM**, **Timeout** & **Retry**.

You can find our implementation of the Proxy LLM pattern in the `llm_proxy.py` file. Here we make sure to not waste tokens by using the cache. 
In a real world implementation said cache would most probably be shared with lots of users and it would expire after a certain amount of time. Obviously, the cache isn't shared between models. This is a great way of showing how important having a well configured proxy can be.

Timeout can be found in the `llm_client.py` file. By using a timeout you can make sure a user isn't left waiting indefinitely wasting resources in an api call that probably cannot be answered at that particular moment. In our case we make sure to give this situation a specific exception.

Finally, the Retry pattern can also be found in the `llm_client.py` file. We make sure to give the client (and our server) more than one attempt to fulfill the request. The random amount of time waited between retries is useful in real world scenarios when there might be network connectivity issues due to a high demand of users trying to access our service at the same time. Of course in this case it is overkill.

