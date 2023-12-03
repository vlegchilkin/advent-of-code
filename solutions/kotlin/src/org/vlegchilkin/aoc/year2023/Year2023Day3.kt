package org.vlegchilkin.aoc.year2023

import org.vlegchilkin.aoc.*


/**
 * 2023/3: Gear Ratios
 */
class Year2023Day3(input: String) : Solution {
  private val space = input.toCSpace { it.takeIf { c -> c != '.' } }

  override fun partAB(): Pair<Int, Int> {
    var partA = 0
    val gears = mutableMapOf<C, MutableList<Int>>()

    for (i in 0..<space.n) {
      var j0: Int? = null
      for (j1 in 0..space.m) {
        if (space[i to j1]?.isDigit() == true) {
          if (j0 == null) j0 = j1
          continue
        }
        if (j0 == null) continue

        val cs = j0..<j1
        val num = cs.fold(0) { a, b -> a * 10 + (space[i to b]!! - '0') }
        val neighbours = cs.flatMap { jx -> space.links(i to jx) { space[it]?.isDigit() == false } }.toSet()
        j0 = null

        neighbours.filter { space[it] == '*' }.forEach { x ->
          gears.getOrPut(x) { mutableListOf() }.add(num)
        }
        if (neighbours.isNotEmpty()) {
          partA += num
        }
      }
    }

    val partB = gears.values.filter { it.size == 2 }.sumOf { it[0] * it[1] }
    return partA to partB
  }

  companion object : Test(2023, 3, { Year2023Day3(it) })
}
