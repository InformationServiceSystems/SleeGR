#
# Copyright (C) 2016, Matthias Heerde <mail@m-heerde.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
import re

from collections import abc
from enum import Enum


class ComparisonStyle(Enum):
    minimum = 0
    maximum = 1
    equity = 2


class MappingValidator:
    """
    MappingValidator enables you to easily validate
    arbitrary mappings(samples) against a reference where you can specify
    the structure the samples should match.
    It is also possible to specify rules for the content of the fields.
    """
    def __init__(self, reference, comparison_style=ComparisonStyle.equity):
        """

        :param reference: referencemapping used to validate other mappings giben in method validate.
        :param comparison_style: Determines the way mappings are compared  to reference.
        """
        self._reference = reference
        self._comparison_style = comparison_style

    @staticmethod
    def _find_all_paths(sample, previous_path=None):
        """
        Finds paths to all keys in the mapping by something like a DFS.
        :param sample: Mapping were paths are searched in.
        :param previous_path: Just used in recursion, by default None
        :return: A list of lists where all paths are stored.
        """
        paths = []
        for key in sample:
            current_path = []
            if previous_path:
                current_path.extend(previous_path)
            current_path.append(key)
            #If the current value ist a mapping, search in this mapping for more paths
            if isinstance(sample[key], abc.Mapping):
                paths.extend(MappingValidator._find_all_paths(sample[key],
                                                              previous_path=current_path))
            paths.append(current_path)
        return sorted(paths, key=lambda k: len(k))

    def _validate_structure(self, mapping):
        """
        Controls the style of the structure-validation(min,max,eq)
        ComparisonStyle.minimum: Are all paths of the reference included in the mapping?
        ComparisonStyle.maximum: Are all paths of the mapping included in the reference?
        ComparisonStyle.equity: Are the paths of the mapping and the reference equal?
        :param mapping: Mapping that is checked.
        :return: True if the structure matches, false otherwise.
        """
        #Call _compare_structure according to comparison_style
        if self._comparison_style == ComparisonStyle.minimum:
            return MappingValidator._compare_structure(mapping, self._reference)
        elif self._comparison_style == ComparisonStyle.maximum:
            return MappingValidator._compare_structure(self._reference, mapping)
        else:
            return MappingValidator._compare_structure(mapping, self._reference) \
                   and MappingValidator._compare_structure(self._reference,
                                                           mapping)

    @staticmethod
    def _compare_structure(sample, reference):
        """
        Checks if the structure of sample at most matches the structure of reference.
        :param sample: The mapping that is going to be validate
        :param reference: The mapping that specifies the structure
        :return: True if sample matches the structure of reference, false otherwise
        """
        paths = MappingValidator._find_all_paths(reference)
        result = True
        for path in paths:
            result = result and MappingValidator._validate_key(sample, path)
            if not result:
                print('refernce;', reference)
                print('sample:', sample)
                print('structure differs at:', path)
                break
        return result

    @staticmethod
    def _validate_key(sample, path):
        """
        Checks if the given path exists in sample
        :param path: Path to a key in the mapping.
        :return: True if path exists, false otherwise.
        """
        mapping_tmp = sample
        for key in path:
            try:
                mapping_tmp = mapping_tmp[key]
            except KeyError:
                print("Tried key::", key)
                return False
            except TypeError:
                print("failed with field:", mapping_tmp)
                return False
        return True

    def _validate_values(self, sample):
        """
        Validate all values in mapping if they match their reference-value.
        :param sample: Mapping that is going to be validated.
        :return: True if all values in sample.
        """
        result = True
        paths = []
        #Search vor necessary paths accorduing to comparison_style
        if self._comparison_style == ComparisonStyle.minimum:
            paths = self._find_all_paths(self._reference)
        else:
            paths = self._find_all_paths(sample)
        # For every path, if it is endling in an key, validate the key
        for path in paths:
            reference_value = MappingValidator._get_value(self._reference,
                                                          list(path))
            mapping_value = MappingValidator._get_value(sample, list(path))
            if isinstance(mapping_value, abc.Mapping):
                continue
            elif isinstance(reference_value, type):
                result = result and isinstance(mapping_value, reference_value)
            elif callable(reference_value):
                result = result and bool(reference_value(mapping_value))
            elif isinstance(reference_value, re._pattern_type):
                result = result and bool(reference_value.match(mapping_value))
            elif isinstance(reference_value, list):
                list_contains_sample_val = False
                for possibility in reference_value:
                    if possibility == mapping_value:
                        list_contains_sample_val = True
                        break
                result = result and list_contains_sample_val
            elif reference_value is Ellipsis:
                result = result and True
            else:
                result = result and False
            if not result:
                print(mapping_value, "(mapping)", "does not match to", reference_value, "(reference)")
                break
        return result

    @staticmethod
    def _get_value(sample, path):
        """
        Search the the value from the given path in the given mapping
        :param sample: Mapping to get the value from.
        :param path: Path to the key.
        :return: The value stored in the mapping at position key.
        """
        if len(path) > 1:
            return MappingValidator._get_value(sample[path.pop(0)], path)
        else:
            return sample[path.pop(0)]

    def validate(self, sample, validate_content=True):
        """
        Validate sample against reference.
        :param sample: Mapping that is going to be validated.
        :param validate_content: Validate structure and the values, or just validate the structure.
        :return: True if sample is valid, False otherwise.
        """
        if validate_content:
            result = self._validate_structure(sample) and self._validate_values(sample)
            return result
        else:
            return self._validate_structure(sample)


if __name__ == '__main__':
    pass
