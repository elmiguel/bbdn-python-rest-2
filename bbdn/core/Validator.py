from schema import Schema, And, Use, Optional, Regex

date_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$'

AnnouncementSchema = Schema({
    "title": str,
    Optional("body"): str,
    Optional("availability"): {
        Optional("duration"): {
            Optional("type"): And(str, lambda s: s in ['Permanent', 'Restricted']),
            Optional("start"): And(str, Regex(date_pattern)),
            Optional("end"): And(str, Regex(date_pattern))
        }
    },
    Optional("showAtLogin"): bool,
    Optional("showInCourses"): bool,
    Optional("created"): And(str, Regex(date_pattern))
})


UserSchema = Schema({
    Optional("externalId"): str,
    Optional("dataSourceId"): str,
    Optional("userName"): str,
    Optional("password"): str,
    Optional("studentId"): str,
    Optional("educationLevel"): And(str, lambda s: s in ['K8', 'HighSchool', 'Freshman', 'Sophomore', 'Junior',
                                                         'Senior', 'GraduateSchool', 'PostGraduateSchool', 'Unknown']),
    Optional("gender"): And(str, lambda s: s in ['Female', 'Male', 'Unknown']),
    Optional("birthDate"): And(str, Regex(date_pattern)),
    Optional("created"): And(str, Regex(date_pattern)),
    Optional("lastLogin"): str,
    Optional("systemRoleIds"): And(list, lambda s: s in ["SystemAdmin", "SystemSupport", "CourseCreator",
                                                         "CourseSupport", "AccountAdmin", "Guest", "User", "Observer",
                                                         "Integration", "Portal"]),
    Optional("availability"): {
        Optional("available"): And(str, Use(str.title), lambda s: s in ["Yes", "No"])
    },
    Optional("name"): {
        "given": str,
        "family": str,
        Optional("middle"): str,
        Optional("other"): str,
        Optional("suffix"): str,
        Optional("title"): str
    },
    Optional("job"): {
        Optional("title"): str,
        Optional("department"): str,
        Optional("company"): str
    },
    Optional("contact"): {
        Optional("homePhone"): str,
        Optional("mobilePhone"): str,
        Optional("businessPhone"): str,
        Optional("businessFax"): str,
        Optional("email"): str,
        Optional("webPage"): str
    },
    Optional("address"): {
        Optional("street1"): str,
        Optional("street2"): str,
        Optional("city"): str,
        Optional("zipCode"): str,
        Optional("country"): str
    },
    Optional("locale"): {
        Optional("id"): str,
        Optional("calendar"): And(str, lambda s: s in ['Gregorian', 'GregorianHijri', 'Hijri',
                                                       'HijriGregorian']),
        Optional("firstDayOfWeek"): And(str, lambda s: s in ['Sunday', 'Monday', 'Tuesday', 'Wednesday',
                                                             'Thursday', 'Friday', 'Saturday'])
    }
})

CourseSchema = Schema({
    Optional("externalId"): str,
    Optional("dataSourceId"): str,
    Optional("courseId"): str,
    Optional("name"): str,
    Optional("description"): str,
    Optional("created"): And(str, Regex(date_pattern)),
    Optional("organization"): bool,
    Optional("ultraStatus"): And(str, lambda s: s in ['Undecided', 'Classic', 'Ultra', 'UltraPreview']),
    Optional("allowGuests"): bool,
    Optional("readOnly"): bool,
    Optional("termId"): str,
    Optional("availability"): {
        Optional("available"): And(str, Use(str.title), lambda s: s in ['Yes', 'No', 'Term']),
        Optional("duration"): {
            Optional("type"): And(str, lambda s: s in ['Continuous', 'DateRange', 'FixedNumDays', 'Term']),
            Optional("start"): And(str, Regex(date_pattern)),
            Optional("end"): And(str, Regex(date_pattern)),
            Optional("daysOfUse"): int
        }

    },
    Optional("enrollment"): {
        Optional("type"): "InstructorLed",
        Optional("start"): And(str, Regex(date_pattern)),
        Optional("end"): And(str, Regex(date_pattern)),
        Optional("accessCode"): str
    },
    Optional("locale"): {
        Optional("id"): str,
        Optional("force"): bool,
    },
    Optional("hasChildren"): bool,
    Optional("parentId"): str
})

ContentsSchema = Schema({
    Optional("title"): str,
    Optional("body"): str,
    Optional("description"): str,
    Optional("created"): And(str, Regex(date_pattern)),
    Optional("position"): int,
    Optional("hasChildren"): bool,
    Optional("hasGradebookColumns"): bool,
    Optional("availability"): {
        Optional("available"): "Yes",
        Optional("allowGuests"): bool,
        Optional("adaptiveRelease"): {
            Optional("start"): And(str, Regex(date_pattern)),
            Optional("end"): And(str, Regex(date_pattern))
        }
    }
})

DataSourceSchema = Schema({
    Optional("externalId"): str,
    Optional("description"): str
})

TermSchema = Schema({
    Optional("externalId"): str,
    Optional("dataSourceId"): str,
    Optional("name"): str,
    Optional("description"): str,
    Optional("availability"): {
        Optional("available"): And(str, Use(str.title), lambda s: s in ['Yes', 'No']),
        Optional("duration"): {
            Optional("type"): And(str, lambda s: s in ['Continuous', 'DateRange', 'FixedNumDays', 'Term']),
            Optional("start"): And(str, Regex(date_pattern)),
            Optional("end"): And(str, Regex(date_pattern)),
            Optional("daysOfUse"): int
        }
    }
})

MembershipSchema = Schema({
    Optional("childCourseId"): str,
    Optional("dataSourceId"): str,
    Optional("created"): And(str, Regex(date_pattern)),
    Optional("availability"): {
        Optional("available"): And(str, Use(str.title), lambda s: s in ['Yes', 'No'])
    },
    Optional("courseRoleId"): And(str, lambda s: s in ["Instructor", "TeachingAssistant", "CourseBuilder", "Grader", "Student",
                                                       "Guest"])
})

SystemSchema = Schema({
    Optional("learn"): {
        Optional("major"): int,
        Optional("minor"): int,
        Optional("patch"): int,
        Optional("build"): str
    }
})

GradebookColumnSchema = Schema({
    Optional("externalId"): str,
    "name": str,
    Optional("description"): str,
    Optional("externalGrade"): bool,
    Optional("created"): And(str, Regex(date_pattern)),
    Optional("score"): {
        "possible": int,
        "decimalPlaces": int
    },
    Optional("availability"): {
        Optional("available"): str
    },
    Optional("grading"): {
        "type": And(str, lambda s: s in ['Attempts', 'Calculated', 'Manual']),
        Optional("due"): And(str, Regex(date_pattern)),
        Optional("attemptsAllowed"): int,
        Optional("scoringModel"): str,
        Optional("anonymousGrading"): {
            "type": And(str, lambda s: s in ['None', 'AfterAllGraded', 'Date']),
            Optional("releaseAfter"): And(str, Regex(date_pattern))
        }
    },
    Optional("contentId"): str
})
