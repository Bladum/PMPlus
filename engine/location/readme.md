# Location Module

This document is the authoritative design and architecture reference for the XCOM/AlienFall location systems. It is intended for validation by AI agents and developers to ensure all planned features and classes are implemented as designed. All subsystem documentation is consolidated here.

## Table of Contents
1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Class Purposes and Details](#class-purposes-and-details)
4. [Integration Guide](#integration-guide)
5. [API Reference](#api-reference)

---

## Overview

The location module implements the core systems for sites, cities, UFOs, and related location logic.

## System Architecture

```
Location Module
├── TSiteType (site_type.py)
├── TSite (site.py)
├── TCity (city.py)
├── TUfoType (ufo_type.py)
├── TUfoScript (ufo_script.py)
├── TUfo (ufo.py)
```

---

## Class Purposes and Details

- **TSiteType:** Defines types of sites.
- **TSite:** Represents a site location.
- **TCity:** Represents a city location.
- **TUfoType:** Defines UFO types.
- **TUfoScript:** Handles UFO scripting logic.
- **TUfo:** Represents a UFO on the map.

---

## Integration Guide

- Use these classes for all site, city, and UFO operations.

---

## API Reference

(See individual files for detailed method signatures.)

