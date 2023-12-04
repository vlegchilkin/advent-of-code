package org.vlegchilkin.aoc.year2020

import org.vlegchilkin.aoc.*

class Year2020Day11(input: String) : Solution {
  private val seats = run {
    val data = input.toList { it.toList().map { c -> c == 'L' } }
    val result = mutableMapOf<Pair<Int, Int>, Int>()
    data.forEachIndexed { rowId, row ->
      row.forEachIndexed { colId, value ->
        if (value) result[rowId to colId] = 0
      }
    }
    result
  }

  private fun simulate(function: (Map<Pair<Int, Int>, Int>) -> Map<Pair<Int, Int>, Int>): Map<Pair<Int, Int>, Int> {
    var prev: Map<Pair<Int, Int>, Int>? = null
    var current: Map<Pair<Int, Int>, Int> = seats
    while (prev != current) {
      prev = current
      current = function(current)
    }
    return current
  }

  override fun partA(): Int {
    return simulate { seats ->
      seats.entries.associate { (seat, occupied) ->
        val neighbours = Direction.all().count { seats.getOrDefault(seat + it, 0) == 1 }
        seat to (occupied == 1 && neighbours < 4 || occupied == 0 && neighbours == 0).toInt()
      }
    }.values.sum()
  }

  override fun partB(): Int {
    val area = seats.keys.area()
    return simulate { seats ->
      seats.entries.associate { (seat, occupied) ->
        val neighbours = Direction.all().count {
          var x = seat + it
          while (x in area && x !in seats) {
            x += it
          }
          seats.getOrDefault(x, 0) == 1
        }
        seat to (occupied == 1 && neighbours < 5 || occupied == 0 && neighbours == 0).toInt()
      }
    }.values.sum()
  }

  companion object : Test(2020, 11, { Year2020Day11(it) })
}


