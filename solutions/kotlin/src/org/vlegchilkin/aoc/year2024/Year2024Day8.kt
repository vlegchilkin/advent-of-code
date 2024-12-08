package org.vlegchilkin.aoc.year2024

import org.vlegchilkin.aoc.*


/**
 * 2024/8: Resonant Collinearity
 */
class Year2024Day8(input: String) : Solution {
  private val space = input.toCSpace { it.takeIf { c -> c != '.' } }

  private fun CSpace<*>.pairs(): Sequence<Pair<C, C>> {
    return this.keys.combinations(2).map { it.toPair() }.filter { (a, b) -> space[a] == space[b] }
  }

  override fun partA(): Any {
    val antinodes = space.pairs().fold(mutableSetOf<C>()) { acc, (a, b) ->
      listOf(a * 2 - b, b * 2 - a)
        .filter { space.isBelongs(it) }
        .forEach { acc.add(it) }
      acc
    }

    return antinodes.size
  }

  override fun partB(): Any {
    fun MutableSet<C>.addTNodes(pos: C, delta: C) {
      val inRangeNodes = generateSequence(pos) { nPos ->
        (nPos + delta).takeIf { space.isBelongs(it) }
      }
      this.addAll(inRangeNodes)
    }

    val antinodes = space.pairs().fold(mutableSetOf<C>()) { acc, (a, b) ->
      acc.addTNodes(a, a-b)
      acc.addTNodes(b, b-a)
      acc
    }

    return antinodes.size
  }

  companion object : Test(2024, 8, { Year2024Day8(it) })
}
