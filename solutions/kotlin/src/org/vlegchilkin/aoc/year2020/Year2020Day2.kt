package org.vlegchilkin.aoc.year2020

import org.vlegchilkin.aoc.Test
import org.vlegchilkin.aoc.Solution

data class Password(val min: Int, val max: Int, val char: Char, val value: String)
class Year2020Day2(input: String) : Solution {
  private val passwords: List<Password>

  init {
    val pattern = """(\d+)-(\d+) ([a-z]): ([a-z]+)""".toRegex()
    passwords = input.trim().split("\n").map {
      val g = pattern.matchEntire(it)!!.groups
      Password(g[1]!!.value.toInt(), g[2]!!.value.toInt(), g[3]!!.value[0], g[4]!!.value)
    }
  }

  override fun partA(): Int {
    return passwords.count { password ->
      val count = password.value.count { it == password.char }
      password.min <= count && count <= password.max
    }
  }

  override fun partB(): Int {
    return passwords.count {
      (it.value[it.min - 1] == it.char) xor (it.value[it.max - 1] == it.char)
    }
  }

  companion object : Test(2020, 2, { Year2020Day2(it) })
}