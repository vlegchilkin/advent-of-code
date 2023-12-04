package org.vlegchilkin.aoc.year2023

import org.vlegchilkin.aoc.*
import kotlin.math.min


/**
 * 2023/4: Scratchcards
 */
class Year2023Day4(input: String) : Solution {
  private val cards = input.toList { card ->
    card.substringAfter(':').split('|').map { it.toList(" ", String::toInt) }
  }

  override fun partA(): Any {
    return cards.sumOf { (left, right) ->
      val score = right.count { it in left }
      if (score > 0) 1 shl (score - 1) else 0
    }
  }

  override fun partB(): Any {
    val counter = IntArray(cards.size) { 1 }
    cards.forEachIndexed { i, (left, right) ->
      val score = right.count { it in left }
      for (j in (i + 1)..min(i + score, cards.size - 1)) {
        counter[j] += counter[i]
      }
    }
    return counter.sum()
  }

  companion object : Test(2023, 4, { Year2023Day4(it) })
}
