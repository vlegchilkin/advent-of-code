package org.vlegchilkin.aoc.year2020

import org.vlegchilkin.aoc.*

enum class PassportRecord(val code: String, val optional: Boolean = false, val validator: (String) -> Boolean = { true }) {
  // Birth Year
  BYR("byr", validator = { s -> s.all { it.isDigit() } && s.toInt() in 1920..2002 }),

  // Issue Year
  IYR("iyr", validator = { it.all { c -> c.isDigit() } && it.toInt() in 2010..2020 }),

  // Expiration Year
  EYR("eyr", validator = { it.all { c -> c.isDigit() } && it.toInt() in 2020..2030 }),

  // Height
  HGT("hgt") {
    override fun validate(value: String): Boolean {
      val matches = """^(\d+)(cm|in)$""".toRegex().matchEntire(value) ?: return false
      val size = matches.groupValues[1].toInt()
      return when (matches.groupValues[2]) {
        "cm" -> size in 150..193
        "in" -> size in 59..76
        else -> false
      }
    }
  },

  // Hair Color
  HCL("hcl", validator = { """^#[0-9a-f]{6}$""".toRegex().matches(it) }),

  // Eye Color
  ECL("ecl", validator = { """^(amb|blu|brn|gry|grn|hzl|oth)$""".toRegex().matches(it) }),

  // Passport ID
  PID("pid", validator = { """^\d{9}$""".toRegex().matches(it) }),

  // Country ID
  CID("cid", optional = true);

  open fun validate(value: String) = validator(value)
}

class Year2020Day4(input: String) : Solution {
  private val passports: List<Map<String, List<String>>>

  init {
    passports = input.trim().split("\n\n").map { it.replace("\n", " ") }.map {
      it.trim().split(" ").map { record ->
        record.split(":").toPair()
      }.groupBy({ d -> d.first }, { d -> d.second })
    }
  }

  override fun partA() = passports.count { it.size == PassportRecord.entries.size - (PassportRecord.CID.code !in it).toInt() }

  override fun partB(): Int {
    return passports.count { data ->
      PassportRecord.entries.all {
        (it.optional && it.code !in data) || (data[it.code]?.size == 1 && it.validate(data[it.code]!![0]))
      }
    }
  }

  companion object : Test(2020, 4, { Year2020Day4(it) })
}