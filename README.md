# Mouse Logger: Mouse Movement & Interaction Tracker

![Mouse Logger Banner](banner.png)

### Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Data Visualization](#data-visualization)
6. [Contribute](#contribute)
7. [License](#license)

## Introduction

Mouse Logger is a passive data collection tool, aimed at recording mouse movements and interactions while users fill out a questionnaire. Built with JavaScript, this tool provides insights into user behavior, tracking parameters such as click frequency, movement speed, and direction. Post data collection, you can visualize this data graphically to derive meaningful insights.

## Features

- **Passive Collection**: Non-intrusive data collection without affecting user experience.
- **Mouse Click Tracking**: Monitor when and where users click within the questionnaire.
- **Speed Tracking**: Observe the speed of mouse movements throughout the session.
- **Direction Tracking**: Understand the direction of mouse movements.
- **Graphical Visualization**: Post-session visual breakdown of user mouse activity.

## Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/morandanieli/mouse_logger.git
    ```

2. **Navigate to the Project Directory**

    ```bash
    cd mouse_logger
    ```

3. **Install Dependencies**

    If the project has any dependencies, make sure to list the installation steps. For instance, if you're using npm:

    ```bash
    npm install
    ```

## Usage

1. **Embed the Logger**

   Embed the JavaScript logger script in your HTML questionnaire page:

   ```html
   <script src="path_to_logger.js"></script>
   ```

2. **Initialize the Logger**

   Initialize the Mouse Logger:

   ```javascript
   MouseLogger.init();
   ```

3. Start your server or open your page to begin collecting data!

## Data Visualization

After collecting data, navigate to the visualization dashboard (e.g., `dashboard.html`). Here, you can:

- View the heatmap of mouse clicks.
- Analyze mouse movement speeds.
- Understand directional preferences.

## Contribute

We welcome contributions! If you find a bug or would like to add a new feature, feel free to open an issue or submit a pull request.

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/myNewFeature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/myNewFeature`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.

---

Made with ❤️ by [Moran Danieli Cohen](https://tenderslab.com) | © 2023 All rights reserved.
