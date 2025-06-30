# Skill Architecture Implementation
The Skill architecture is comprised of the Skill Base Class to serve as a common template for all implemented skills, a Skill Metaclass which acts as a singleton factory and collection registry.  Together, these two classes form a system where derivation of a specific skill implementation from the Skill base class provides the following functionality:

1.  Pydantic based runtime type checking
2.  A set of required fields which all skills must implement:
    - name
    - description
    - icon (embedded binary representation of skill's icon)
    - id (a unique, deterministic UUID for the named skill)
    - tool (function to be called by the LLM to implement the skill)

## Skill Class
Defines the required fields for all derived skills:
- name:  A string representing the skill name formatted for display in the frontend.  (Spaces, capitalization, etc..). Singleton checkin is enforced on the skill name.  
- description:  A string with a short description of what the skill is meant to do.
- icon:  A string containing a utf-8, base64 encoded binary representation of an icon suitable for transmission via HTTP.
- id:  A _deterministic_ UUID based on the skill name.
- tool:  A function instantiated as a langchain_core.tools StructuredTool object which can be used directly by Langchain/Graph's toolcalling callable architecture.

The skill class also implements two helper methods:

- __hash__: Allowing a Skill to be hashed based on the skill id.
- model_dump: A custom serializer to properly dump only the serializible fields for JSON output.

## SkillMeta Class
The SkillMeta class derives from a Pydantic base Metaclass, carrying forward Pydantic's type checking and validation features.  Additionally the SkillMeta class implements the singleton factory functionality and centralizes the Skill class registry and collection tracking functionality.

- _instances:  Class field storing the list of instantiated Skill derived classes.

- _collections:  Class field storing a dictionary mapping named collections to sets of skills.  (e.g. "Default" or indexing by specific AgentIDs for custom agents)

The SkillMeta class implements the methods necessary to interact with skill collections as well as retrieiving all instantiated skills:

- store_collection:  Maps a collection name (e.g. "default") to a list of Skill names to be associated with the collection name.  Includes instantiation checks for skills actually existing as well as checks for duplication of a named collection.

- get_collection:  Returns a list of Skill objects (NOT skill names) which are associated with the given collection name.

- get_tools:  Returns a list of _just the tools_ from a collection of Skill objects suitable for being bound to a tool-calling LLM model.

- get_all_skills:  Returns the list of all currently instantiated skills.

## skill_loader.py
In order to simplify use and skill discovery, the file _skill_loader.py_ provides the logic necessary to automatically discover and load every skill which is properly defined (i.e. defined as a derived class from Skill) within a given directory.

Calling load_skills will parse the "tools" directory, find all regular python files within the directory, and for every defined object derived from the Skill class, attempt to instantiate the discovered skill.  If the skill cannot be instantiated an error message is generated before progressing to trying to instantiate the next skill.


## Tools directory
Each tool in the tools directory has been recast as a derived class from the Skill base class.  Note that the singleton nature of the class is based on the class 'name' field, NOT the class name itself.  (Potentially useful for having skills which implement the same logic with different LLMs/prompts)

### Icons subdirectory
The icons subdirectory holds the binary icons which can be associated and encoded within the skill icon fields.  This is accomplished with the 'encode_icon_url_safe_utf8' function in icon_process.py for easy association of icon files to implemented skills.  This is useful for, e.g., associating a generic icon with a series of skills.  (i.e. You want all financially oriented skills to have a specific icon which contains currency symbols for quick visual identification of skill classes.)