package org.vlegchilkin.aoc.year2023

import org.vlegchilkin.aoc.*
import kotlin.math.absoluteValue


/**
 * 2023/11: Cosmic Expansion
 */
class Year2023Day11(input: String) : Solution {
  private val space = input.toCSpace()

  private fun getExpansion(gravitationEffect: Int): Pair<List<Long>, List<Long>> {
    var total = 0L
    val rExp = space.rows.map { r ->
      total += (space.cols.all { c -> (r to c) !in space }).toInt() * (gravitationEffect - 1)
      total
    }
    total = 0L
    val cExp = space.cols.map { c ->
      total += (space.rows.all { r -> (r to c) !in space }).toInt() * (gravitationEffect - 1)
      total
    }
    return rExp to cExp
  }

  private fun sumOfDistances(gravitationEffect: Int): Long {
    val (rExp, cExp) = getExpansion(gravitationEffect)
    val distances = space.keys.combinations(2).map { (a, b) ->
      (a manhattanTo b) + (rExp[a.first] - rExp[b.first]).absoluteValue + (cExp[a.second] - cExp[b.second]).absoluteValue
    }
    return distances.sum()
  }

  override fun partA(): Long {
    return sumOfDistances(2)
  }

  override fun partB(): Any {
    return sumOfDistances(1000000)
  }

  companion object : Test(2023, 11, { Year2023Day11(it) })
}
