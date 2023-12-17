package org.vlegchilkin.aoc.year2023

import org.vlegchilkin.aoc.*
import org.vlegchilkin.aoc.Direction.*


/**
 * 2023/14: Parabolic Reflector Dish
 */
class Year2023Day14(input: String) : Solution {
  private val space = input.toCSpace { it.takeIf { it != '.' } }

  private fun roll(space: CSpace<Char>, direction: Direction) {
    val comparator = when (direction) {
      N -> compareBy { it.first }
      S -> compareBy<C> { it.first }.reversed()
      W -> compareBy { it.second }
      E -> compareBy<C> { it.second }.reversed()
      else -> throw IllegalArgumentException()
    }
    val roundedRocks = space.filterValues { it == 'O' }.keys.sortedWith(comparator)
    for (initPos in roundedRocks) {
      var endPos = initPos
      while (space.isEmpty(endPos + direction)) endPos += direction
      if (initPos != endPos) {
        space[endPos] = space[initPos]!!
        space.remove(initPos)
      }
    }
  }

  private fun weight(space: CSpace<Char>): Int {
    return space.filterValues { it == 'O' }.keys.sumOf {
      space.rows.last - it.first + 1
    }
  }

  override fun partA(): Any {
    val space = this.space.clone()
    roll(space, N)
    return weight(space)
  }

  override fun partB(): Int {
    val space = this.space.clone()
    fun runCycle() {
      for (d in listOf(N, W, S, E)) roll(space, d)
    }

    fun calcHash(): String {
      return space.filterValues { it == 'O' }.keys.map { it.first * space.rowsCount + it.second }.sorted().toString()
    }

    val hashes = mutableMapOf<String, Int>()
    val weights = mutableMapOf<Int, Int>()
    val totalCycles = 1000000000
    var (cycle, hash) = 0 to calcHash()
    while (hash !in hashes && cycle < totalCycles) {
      hashes[hash] = cycle
      weights[cycle] = weight(space)
      runCycle()
      cycle += 1
      hash = calcHash()
    }

    val finishWeight = hashes[hash]?.let { prevCycle ->
      val len = cycle - prevCycle
      val destCycle = ((totalCycles - cycle) % len) + prevCycle
      weights[destCycle]
    } ?: weight(space)

    return finishWeight
  }

  companion object : Test(2023, 14, { Year2023Day14(it) })
}
