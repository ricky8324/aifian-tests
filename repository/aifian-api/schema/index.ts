import { z } from 'zod';

const transactionDetailBaseSchema = z.object({
  id: z.string().uuid(),
  type: z.enum(['LIQUOR']),
  action: z.enum(['BUY', 'RESELL', 'CLAIM']),
  title: z.string(),
  created_at: z.string().datetime(),
  status: z.enum(['PROCESSING', 'COMPLETED', 'CANCELLED', 'TRANSFERRING']),
  other: z.string(),
});

const liquorBuyTransactionSchema = transactionDetailBaseSchema.extend({
  currency: z.enum(['TWD', 'USD']),
  amount: z.number(),
  detail: z.object({
    title: z.string(),
    product_id: z.string(),
    product_name: z.string(),
    currency: z.enum(['TWD', 'USD']),
    total_amount: z.number(),
    total_qty: z.number(),
    filled_amount: z.number(),
    filled_qty: z.number(),
    unit_price: z.number(),
    reward_used: z
      .object({
        value: z.number(),
        amount: z.number(),
      })
      .optional(),
    final_amount: z.number(),
    payment_option: z.string(),
    completed_at: z.string().datetime().nullable(),
    canceled_reason: z.string().optional(),
  }),
});

const liquorResellTransactionSchema = transactionDetailBaseSchema.extend({
  currency: z.enum(['TWD', 'USD']),
  amount: z.number(),
  detail: z.object({
    title: z.string(),
    product_id: z.string(),
    product_name: z.string(),
    currency: z.enum(['TWD', 'USD']),
    total_amount: z.number(),
    total_qty: z.number(),
    filled_amount: z.number(),
    filled_qty: z.number(),
    unit_price: z.number(),
    process_fee: z.number(),
    storage_fee: z.number(),
    final_amount: z.number(),
    filled_at: z.string().datetime().optional(),
    completed_at: z.string().datetime().optional(),
    canceled_reason: z.string().optional(),
    transfer_error: z.string().optional(),
  }),
});

const liquorClaimTransactionSchema = transactionDetailBaseSchema;

const portfolioSummarySchema = z.object({
  portfolio: z.array(
    z.object({
      product_id: z.string(),
      product_name: z.string(),
      qty: z.number(),
      asset_value: z.number(),
      return: z.object({
        delta: z.number(),
        pct: z.number(),
      }),
      image_url: z.string().url(),
      image_bg_color: z.string(),
    }),
  ),
  market: z.object({
    bundle: z
      .array(
        z.object({
          product_id: z.string(),
          product_name: z.string(),
          product_price: z.number(),
          return: z.object({
            delta: z.number(),
            pct: z.number(),
          }),
          image_url: z.string().url(),
          image_bg_color: z.string(),
        }),
      )
      .nullable(),
    single: z
      .array(
        z.object({
          product_id: z.string(),
          product_name: z.string(),
          product_price: z.number(),
          return: z.object({
            delta: z.number(),
            pct: z.number(),
          }),
          image_url: z.string().url(),
          image_bg_color: z.string(),
        }),
      )
      .nullable(),
  }),
  faq: z
    .object({
      articles: z.array(
        z.object({
          title: z.string(),
          image_url: z.string().url(),
          article_id: z.string(),
        }),
      ),
    })
    .optional(),
  promotion: z
    .object({
      image_url: z.string().url(),
      product_id: z.string(),
      product_price: z.number(),
    })
    .optional(),
});

export {
  liquorBuyTransactionSchema,
  liquorResellTransactionSchema,
  liquorClaimTransactionSchema,
  portfolioSummarySchema,
};
