//! Optional SolProbe on-chain registry (scaffold).
//!
//! This program is intentionally minimal — it is a placeholder for a future
//! registry of RPC providers and watch targets.

use anchor_lang::prelude::*;

declare_id!("SOLPROBE_REGISTRY_PROGRAM_ID");

#[program]
pub mod solprobe_registry {
    use super::*;

    pub fn initialize(ctx: Context<Initialize>) -> Result<()> {
        let registry = &mut ctx.accounts.registry;
        registry.authority = ctx.accounts.authority.key();
        registry.entry_count = 0;
        Ok(())
    }
}

#[account]
#[derive(Default)]
pub struct Registry {
    pub authority: Pubkey,
    pub entry_count: u32,
}

#[derive(Accounts)]
pub struct Initialize<'info> {
    #[account(init, payer = authority, space = 8 + 32 + 4)]
    pub registry: Account<'info, Registry>,
    #[account(mut)]
    pub authority: Signer<'info>,
    pub system_program: Program<'info, System>,
}
