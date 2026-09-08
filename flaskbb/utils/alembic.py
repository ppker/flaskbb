from __future__ import annotations

import os
import typing as t

from alembic.config import Config
from flask import current_app
from flask_alembic import Alembic as FlaskAlembic


class Alembic(FlaskAlembic):
    @property
    @t.override
    def config(self) -> Config:
        """Get the Alembic :class:`~alembic.config.Config` for the
        current app.
        """
        cache = self._get_cache()

        if cache.config is not None:
            return cache.config

        cache.config = c = Config()
        script_location = t.cast(str, current_app.config["ALEMBIC"]["script_location"])

        if not os.path.isabs(script_location) and ":" not in script_location:
            script_location = os.path.join(current_app.root_path, script_location)

        version_locations: list[str] = [script_location]

        for item in current_app.config["ALEMBIC"]["version_locations"]:
            version_location = t.cast(str, item if isinstance(item, str) else item[1])

            if not os.path.isabs(version_location) and ":" not in version_location:
                version_location = os.path.join(current_app.root_path, version_location)

            version_locations.append(version_location)

        c.set_main_option("script_location", script_location)
        c.set_main_option("path_separator", current_app.config["ALEMBIC"]["path_separator"])
        # path_separator is always set above, so this is never None
        path_sep = t.cast(str, c._get_file_separator_char("path_separator"))
        c.set_main_option(
            "version_locations",
            path_sep.join(version_locations),
        )

        for key, value in current_app.config["ALEMBIC"].items():
            if key in ("script_location", "version_locations", "path_separator"):
                continue

            if isinstance(value, dict):
                for inner_key, inner_value in value.items():
                    c.set_section_option(key, inner_key, inner_value)
            else:
                c.set_main_option(key, value)

        if len(self.metadatas) > 1:
            # Add the names used by the multidb template.
            c.set_main_option("databases", ", ".join(self.metadatas))

        return cache.config
