package org.vlegchilkin.aoc.year2020

import org.vlegchilkin.aoc.Test
import org.vlegchilkin.aoc.Solution
import org.vlegchilkin.aoc.toPair
import org.vlegchilkin.aoc.toList

class Year2020Day25(input: String) : Solution {
  private val values = input.toList { it.toInt() }.toPair()

  override fun partA(): Int {
    var x = 1
    var cardLoop = 0
    while (x != values.first) {
      cardLoop += 1
      x = (1L * x * PUB_KEY_SUBJECT % MODULO).toInt()
    }

    x = 1
    repeat(cardLoop) {
      x = (1L * x * values.second % MODULO).toInt()
    }

    return x
  }


  companion object : Test(2020, 25, { Year2020Day25(it) }) {
    const val PUB_KEY_SUBJECT = 7
    const val MODULO = 20201227
  }
}