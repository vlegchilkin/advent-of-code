package org.vlegchilkin.aoc.year2023

import org.vlegchilkin.aoc.*


/**
 * 2023/7: Camel Cards
 */
class Year2023Day7(input: String) : Solution {
  private val hands = input.toList { h ->
    h.toList(" ") { it }.toObject(Hand::class)
  }

  data class Hand(val cards: String, val bet: Int)
  enum class HandType {
    FIVE, FOUR, FULL_HOUSE, THREE, TWO_PAIR, ONE_PAIR, HIGH_CARD;

    companion object {
      fun of(hand: String): HandType {
        val groups = hand.groupingBy { it }.eachCount().values.sortedDescending()
        return when (groups.size) {
          1 -> FIVE
          2 -> if (groups[0] == 4) FOUR else FULL_HOUSE
          3 -> if (groups[0] == 3) THREE else TWO_PAIR
          4 -> ONE_PAIR
          else -> HIGH_CARD
        }
      }
    }
  }

  private fun totalWinnings(deck: String, typeOf: (String) -> HandType): Int {
    fun powerOf(hand: String): Int {
      val type = typeOf(hand)
      val cp = hand.map { deck.indexOf(it) }
      return cp.fold(type.ordinal) { acc, x -> (acc shl 4) + x }
    }

    val handPowers = hands.map { it to powerOf(it.cards) }
    return handPowers
      .sortedWith(compareBy { it.second }).asReversed()
      .mapIndexed { i, (hand, _) -> hand.bet * (i + 1) }.sum()
  }


  override fun partA(): Any {
    return totalWinnings("AKQJT98765432") { hand ->
      HandType.of(hand)
    }
  }

  override fun partB(): Any {
    val deck = "AKQT98765432J"
    return totalWinnings(deck) { hand ->
      deck.minOf { HandType.of(hand.replace('J', it)) }
    }
  }

  companion object : Test(2023, 7, { Year2023Day7(it) })
}
